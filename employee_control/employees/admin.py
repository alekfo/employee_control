from django.contrib import admin

from .models import Employee, Station, Task, Knowledge, Comment, Link, Attachment

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = "pk", "user", "position", "phone"

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = "pk", "station", "description", "status", "responsible_organization", "responsible_user", "registration_date", "due_date"

    list_select_related = ('station', 'responsible_user')

@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = "pk", "name", "road", "description", "latitude", "longitude", "created_at"
