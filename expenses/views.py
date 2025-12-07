from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Sum, Q
from django.contrib.auth.models import User
import csv
from datetime import date
from .models import (
    Expense, Category, RecurringExpense, Budget,
    Goal, Notification, UserProfile
)

# ------------------------------------------------------
# AUTH
# ------------------------------------------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dash")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "expenses/login.html")


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return render(request, "expenses/registration.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, "expenses/registration.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return render(request, "expenses/registration.html")

        User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        messages.success(request, "Account created successfully! Please login.")
        return redirect("login")

    return render(request, "expenses/registration.html")


def home(request):
    return render(request, "expenses/home.html")


# ------------------------------------------------------
# DASHBOARD
# ------------------------------------------------------
@login_required
def dash(request):
    today = timezone.now().date()
    month_start = today.replace(day=1)

    today_spent = Expense.objects.filter(
        user=request.user, date=today, status="PAID"
    ).aggregate(total=Sum("amount"))["total"] or 0

    month_spent = Expense.objects.filter(
        user=request.user, date__gte=month_start, status="PAID"
    ).aggregate(total=Sum("amount"))["total"] or 0

    budgets = Budget.objects.filter(user=request.user)
    total_budget = sum(b.amount for b in budgets)
    remaining_budget = total_budget - month_spent
    estimated_savings = remaining_budget

    used_percent = (month_spent * 100 / total_budget) if total_budget > 0 else 0

    recent_expenses = Expense.objects.filter(
        user=request.user
    ).order_by("-date")[:5]

    top_categories = (
        Expense.objects.filter(user=request.user)
        .values("category__name")
        .annotate(total=Sum("amount"))
        .order_by("-total")[:5]
    )

    goals = Goal.objects.filter(user=request.user)

    notifications_unread = Notification.objects.filter(
        user=request.user, is_read=False
    ).count()

    return render(request, "expenses/dash.html", {
        "today": today,
        "today_spent": today_spent,
        "month_spent": month_spent,
        "total_budget": total_budget,
        "remaining_budget": remaining_budget,
        "estimated_savings": estimated_savings,
        "used_percent": used_percent,
        "recent_expenses": recent_expenses,
        "top_categories": top_categories,
        "goals": goals,
        "notifications_unread_count": notifications_unread,
    })


# ------------------------------------------------------
# EXPENSES
# ------------------------------------------------------
@login_required
def expenses_list(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    categories = Category.objects.filter(user=request.user)

    search = request.GET.get("search", "")
    category_id = request.GET.get("category", "")
    status = request.GET.get("status", "")

    if search:
        expenses = expenses.filter(
            Q(title__icontains=search) |
            Q(amount__icontains=search) |
            Q(date__icontains=search) |
            Q(category__name__icontains=search)
        )

    if category_id:
        expenses = expenses.filter(category__id=category_id)

    if status:
        expenses = expenses.filter(status=status)

    return render(request, "expenses/expenses_list.html", {
        "expenses": expenses,
        "categories": categories,
    })


@login_required
def expense_add(request):
    categories = Category.objects.filter(user=request.user)

    if request.method == "POST":
        Expense.objects.create(
            user=request.user,
            title=request.POST["title"],
            amount=request.POST["amount"],
            category_id=request.POST.get("category"),
            date=request.POST["date"],
            note=request.POST.get("note", ""),
            status=request.POST.get("status", "PAID"),
        )
        messages.success(request, "Expense added successfully!")
        return redirect("expenses_list")

    return render(request, "expenses/expense_add.html", {
        "categories": categories
    })


@login_required
def expense_edit(request, id):
    expense = get_object_or_404(Expense, id=id, user=request.user)
    categories = Category.objects.filter(user=request.user)

    if request.method == "POST":
        expense.title = request.POST["title"]
        expense.amount = request.POST["amount"]
        expense.category_id = request.POST.get("category")
        expense.date = request.POST["date"]
        expense.note = request.POST.get("note", "")
        expense.status = request.POST.get("status", "PAID")
        expense.save()

        messages.success(request, "Expense updated successfully!")
        return redirect("expenses_list")

    return render(request, "expenses/expense_edit.html", {
        "expense": expense,
        "categories": categories
    })


@login_required
def expense_view(request, id):
    expense = get_object_or_404(Expense, id=id, user=request.user)
    return render(request, "expenses/expense_view.html", {"expense": expense})


@login_required
def expense_delete(request, id):
    expense = get_object_or_404(Expense, id=id, user=request.user)
    expense.delete()
    messages.success(request, "Expense deleted.")
    return redirect("expenses_list")


@login_required
def pending_expenses(request):
    pending = Expense.objects.filter(
        user=request.user, status="PENDING"
    )
    return render(request, "expenses/pending_expenses.html", {"pending": pending})


# ------------------------------------------------------
# RECURRING EXPENSES
# ------------------------------------------------------
@login_required
def recurring_list(request):
    recurring = RecurringExpense.objects.filter(user=request.user)
    return render(request, "expenses/recurring_list.html", {"recurring": recurring})


@login_required
def recurring_add(request):
    categories = Category.objects.filter(user=request.user)

    if request.method == "POST":
        RecurringExpense.objects.create(
            user=request.user,
            category_id=request.POST.get("category"),
            title=request.POST.get("title"),
            amount=request.POST.get("amount"),
            cycle=request.POST.get("cycle"),
            next_date=request.POST.get("next_date"),
        )
        messages.success(request, "Recurring expense added!")
        return redirect("recurring_list")

    return render(request, "expenses/recurring_form.html", {
        "form_title": "Add",
        "button_text": "Save",
        "r": None,
        "categories": categories,
        "today": date.today().isoformat(),   # REQUIRED
    })


@login_required
def recurring_edit(request, id):
    r = get_object_or_404(RecurringExpense, id=id, user=request.user)

    if request.method == "POST":
        r.title = request.POST["title"]
        r.amount = request.POST["amount"]
        r.cycle = request.POST["cycle"]
        r.next_date = request.POST["next_date"]
        r.save()

        messages.success(request, "Recurring updated!")
        return redirect("recurring_list")

    return render(request, "expenses/recurring_form.html", {
        "form_title": "Edit",
        "button_text": "Update",
        "r": r,
    })


@login_required
def recurring_delete(request, id):
    r = get_object_or_404(RecurringExpense, id=id, user=request.user)
    r.delete()
    messages.success(request, "Recurring deleted.")
    return redirect("recurring_list")


# ------------------------------------------------------
# CATEGORIES
# ------------------------------------------------------
@login_required
def categories_list(request):
    categories = Category.objects.filter(user=request.user)
    return render(request, "expenses/categories_list.html", {"categories": categories})


@login_required
def category_add(request):
    if request.method == "POST":
        Category.objects.create(
            user=request.user,
            name=request.POST["name"],
            icon=request.POST.get("icon", "")
        )
        messages.success(request, "Category added!")
        return redirect("categories_list")

    return render(request, "expenses/category_form.html", {
        "form_title": "Add",
        "button_text": "Save",
    })


@login_required
def category_edit(request, id):
    c = get_object_or_404(Category, id=id, user=request.user)

    if request.method == "POST":
        c.name = request.POST["name"]
        c.icon = request.POST.get("icon", "")
        c.save()

        messages.success(request, "Category updated!")
        return redirect("categories_list")

    return render(request, "expenses/category_form.html", {
        "form_title": "Edit",
        "button_text": "Update",
        "category": c,
    })


@login_required
def category_delete(request, id):
    c = get_object_or_404(Category, id=id, user=request.user)
    c.delete()
    messages.success(request, "Category deleted.")
    return redirect("categories_list")


# ------------------------------------------------------
# BUDGETS
# ------------------------------------------------------
@login_required
def budgets_list(request):
    today = timezone.now().date()
    month_start = today.replace(day=1)

    budgets = Budget.objects.filter(user=request.user, month=month_start)
    total_budget = sum(b.amount for b in budgets)

    return render(request, "expenses/budgets_list.html", {
        "budgets": budgets,
        "total_budget": total_budget,
    })


@login_required
def budget_add(request):
    categories = Category.objects.filter(user=request.user)

    if request.method == "POST":
        Budget.objects.create(
            user=request.user,
            category_id=request.POST["category"],
            amount=request.POST["amount"],
            month=request.POST["month"] + "-01"
        )
        messages.success(request, "Budget added!")
        return redirect("budgets_list")

    return render(request, "expenses/budget_form.html", {
        "categories": categories,
        "form_title": "Add",
        "button_text": "Save",
        "budget": None
    })


@login_required
def budget_edit(request, id):
    budget = get_object_or_404(Budget, id=id, user=request.user)
    categories = Category.objects.filter(user=request.user)

    if request.method == "POST":
        budget.category_id = request.POST["category"]
        budget.amount = request.POST["amount"]
        budget.month = request.POST["month"] + "-01"
        budget.save()

        messages.success(request, "Budget updated!")
        return redirect("budgets_list")

    return render(request, "expenses/budget_form.html", {
        "categories": categories,
        "form_title": "Edit",
        "button_text": "Update",
        "budget": budget
    })


@login_required
def budget_delete(request, id):
    budget = get_object_or_404(Budget, id=id, user=request.user)
    budget.delete()
    messages.success(request, "Budget deleted.")
    return redirect("budgets_list")


@login_required
def set_budget(request):
    categories = Category.objects.filter(user=request.user)
    today = timezone.now().date()
    month = today.replace(day=1)

    budget = Budget.objects.filter(user=request.user, month=month).first()

    if request.method == "POST":
        category_id = request.POST["category"]
        amount = request.POST["amount"]

        if budget:
            budget.category_id = category_id
            budget.amount = amount
            budget.save()
            messages.success(request, "Budget updated successfully!")
        else:
            Budget.objects.create(
                user=request.user,
                category_id=category_id,
                amount=amount,
                month=month
            )
            messages.success(request, "Budget set successfully!")

        return redirect("budgets_list")

    return render(request, "expenses/set_budget.html", {
        "categories": categories,
        "budget": budget
    })


# ------------------------------------------------------
# MONTHLY OVERVIEW
# ------------------------------------------------------
@login_required
def monthly_overview(request):
    today = timezone.now().date()
    month_start = today.replace(day=1)

    month_spent = Expense.objects.filter(
        user=request.user, date__gte=month_start, status="PAID"
    ).aggregate(total=Sum("amount"))["total"] or 0

    top_categories = (
        Expense.objects.filter(user=request.user, date__gte=month_start)
        .values("category__name")
        .annotate(total=Sum("amount"))
        .order_by("-total")
    )

    budgets = Budget.objects.filter(user=request.user)
    total_budget = sum(b.amount for b in budgets)
    remaining_budget = total_budget - month_spent

    return render(request, "expenses/monthly_overview.html", {
        "month_spent": month_spent,
        "top_categories": top_categories,
        "remaining_budget": remaining_budget,
    })


# ------------------------------------------------------
# MONTHLY REPORT
# ------------------------------------------------------
@login_required
def monthly_report(request):
    today = timezone.now().date()
    month_start = today.replace(day=1)

    month_spent = Expense.objects.filter(
        user=request.user, date__gte=month_start
    ).aggregate(total=Sum("amount"))["total"] or 0

    top_categories = (
        Expense.objects.filter(user=request.user, date__gte=month_start)
        .values("category__name")
        .annotate(total=Sum("amount"))
        .order_by("-total")
    )

    return render(request, "expenses/monthly_report.html", {
        "month_spent": month_spent,
        "top_categories": top_categories,
        "net_savings": 0,
        "total_income": 0,
    })


# ------------------------------------------------------
# PROFILE
# ------------------------------------------------------
@login_required
def profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        request.user.email = request.POST["email"]
        request.user.save()

        profile.currency = request.POST["currency"]
        profile.save()

        messages.success(request, "Profile updated!")
        return redirect("profile")

    return render(request, "expenses/profile.html", {
        "profile": profile
    })


# ------------------------------------------------------
# NOTIFICATIONS
# ------------------------------------------------------
@login_required
def notifications(request):
    notes = Notification.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "expenses/notifications.html", {"notifications": notes})


@login_required
def notifications_mark_all_read(request):
    Notification.objects.filter(user=request.user).update(is_read=True)
    return redirect("notifications")


@login_required
def notification_toggle_read(request, id):
    n = get_object_or_404(Notification, id=id, user=request.user)
    n.is_read = not n.is_read
    n.save()
    return redirect("notifications")


# ------------------------------------------------------
# EXPORT CSV
# ------------------------------------------------------
@login_required
def export_csv(request):
    expenses = Expense.objects.filter(user=request.user)

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=expenses.csv"
    
    writer = csv.writer(response)
    writer.writerow(["Title", "Category", "Amount", "Date", "Status"])

    for e in expenses:
        writer.writerow([
            e.title,
            e.category.name if e.category else "-",
            e.amount,
            e.date,
            e.status
        ])

    return response
    
