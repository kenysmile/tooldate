from django.contrib import admin
from .models import ToolDate, ToolDateDetails

class ToolDateAdmin(admin.ModelAdmin):
    list_display= ["tool_date_id", "lst_extra_hours", "start_date"]
    search_fields= ["tool_date_id", "start_date"]

class ToolDateDetailsAdmin(admin.ModelAdmin):
    list_display= ["tool_date", "extra_hours", "start_date", "end_date", "time_out"]
    search_fields= ["tool_date", "start_date", "end_date"]


# Register your models here.
admin.site.register(ToolDate, ToolDateAdmin)
admin.site.register(ToolDateDetails, ToolDateDetailsAdmin)

