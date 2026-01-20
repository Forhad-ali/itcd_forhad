from django.contrib import admin
from import_export.admin import ExportMixin

from .models import System

class SystemAdmin(admin.ModelAdmin):
    list_display = ('code', 'title')

admin.site.register(System, SystemAdmin)
