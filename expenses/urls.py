from django.urls import path
from . import views

urlpatterns = [
    

    # Dashboard
    path('', views.home ,name= 'home'),
    path("dash/", views.dash, name="dash"),
    path('login/', views.login_view, name="login"),
    path('register/', views.register, name="register"),

    # Expenses
    path("expenses/", views.expenses_list, name="expenses_list"),
    path("expense/add/", views.expense_add, name="expense_add"),
    path("expense/<int:id>/edit/", views.expense_edit, name="expense_edit"),
    path("expense/<int:id>/view/", views.expense_view, name="expense_view"),
    path("expense/<int:id>/delete/", views.expense_delete, name="expense_delete"),
    path("expenses/pending/", views.pending_expenses, name="pending_expenses"),

    # Recurring Expenses
    path("recurring/", views.recurring_list, name="recurring_list"),
    path("recurring/add/", views.recurring_add, name="recurring_add"),
    path("recurring/<int:id>/edit/", views.recurring_edit, name="recurring_edit"),
    path("recurring/<int:id>/delete/", views.recurring_delete, name="recurring_delete"),

    # Categories
    path("categories/", views.categories_list, name="categories_list"),
    path("category/add/", views.category_add, name="category_add"),
    path("category/<int:id>/edit/", views.category_edit, name="category_edit"),
    path("category/<int:id>/delete/", views.category_delete, name="category_delete"),

    # Budgets
    path("budgets/", views.budgets_list, name="budgets_list"),
    path("budget/add/", views.budget_add, name="budget_add"),
    path("budget/<int:id>/edit/", views.budget_edit, name="budget_edit"),
    path("budget/<int:id>/delete/", views.budget_delete, name="budget_delete"),
    path("budget/set/", views.set_budget, name="set_budget"),

    # Monthly Overview
    path("overview/", views.monthly_overview, name="monthly_overview"),

    # Monthly Report
    path("report/", views.monthly_report, name="monthly_report"),

    # Notifications
    path("notifications/", views.notifications, name="notifications"),
    path("notifications/mark-all/", views.notifications_mark_all_read, name="notifications_mark_all_read"),
    path("notification/<int:id>/toggle/", views.notification_toggle_read, name="notification_toggle_read"),

    # Profile
    path("profile/", views.profile, name="profile"),

    # Export CSV
    path("export/", views.export_csv, name="export_csv"),
]