from django.contrib import admin

from .models import Duty


@admin.register(Duty)
class DutyAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'done_status', 'created_date',)
    list_filter = ('author', 'done_status','deadline_date',)
    search_fields = ('author', 'title',)