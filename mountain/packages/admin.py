from django.contrib import admin
from django.db import models
from django.forms import widgets

from mountain.packages.models import Package, PackageRelation


class RelationInline(admin.TabularInline):
    model = PackageRelation
    extra = 0
    formfield_overrides = {
        models.TextField: {'widget': widgets.TextInput},
    }


class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'summary', 'section', 'type')
    list_filter = ('section',)
    ordering = ('name',)
    search_fields = ('name',)
    inlines = [RelationInline]

admin.site.register(Package, PackageAdmin)
