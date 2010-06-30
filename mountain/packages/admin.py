from django.contrib import admin

from mountain.packages.models import *

class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'summary', 'section', 'type')
    list_filter = ('section',)
    ordering = ('name',)
    search_fields = ('name',)

admin.site.register(PackageHash, PackageAdmin)
