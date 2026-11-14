from django.contrib import admin

from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("company", "position", "status", "applied_date", "user")
    list_filter = ("status",)
    search_fields = ("company", "position")
