from django.contrib import admin
from .models import UserProfile, Category, Expense, RecurringExpense, Budget, Goal, Notification, ExportLog


admin.site.site_header = "Expense Manager Admin"
admin.site.site_title = "Expense Management System"
admin.site.index_title = "Backend Control Panel"

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "currency")
    search_fields = ("user__username", "role")
    list_filter = ("role", "currency")
    ordering = ("user",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "icon")
    search_fields = ("name", "user__username")
    list_filter = ("user",)
    ordering = ("name",)


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "category", "amount", "date", "status")
    search_fields = ("title", "category__name", "user__username")
    list_filter = ("status", "category", "user", "date")
    list_editable = ("status",)
    ordering = ("-date",)
    date_hierarchy = "date"


@admin.register(RecurringExpense)
class RecurringExpenseAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "category", "amount", "cycle", "next_date")
    search_fields = ("title", "category__name", "user__username")
    list_filter = ("cycle", "category", "user")
    ordering = ("next_date",)
    date_hierarchy = "next_date"


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ("category", "user", "amount", "month")
    search_fields = ("category__name", "user__username")
    list_filter = ("category", "month")
    ordering = ("-month",)
    date_hierarchy = "month"


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "target_amount", "current_progress", "deadline")
    search_fields = ("title", "user__username")
    list_filter = ("deadline",)
    ordering = ("deadline",)
    date_hierarchy = "deadline"


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("message", "user", "created_at", "is_read")
    search_fields = ("message", "user__username")
    list_filter = ("is_read", "created_at")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)


@admin.register(ExportLog)
class ExportLogAdmin(admin.ModelAdmin):
    list_display = ("user", "exported_at")
    search_fields = ("user__username",)
    ordering = ("-exported_at",)
    readonly_fields = ("exported_at",)