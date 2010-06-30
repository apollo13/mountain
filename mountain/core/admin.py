from django.contrib import admin
from django.utils.simplejson import dumps

from mountain.core.models import *
from mountain.core.utils import hash_types

def force_resync(modeladmin, request, queryset):
    for comp in queryset:
        Message.objects.create(computer=comp, message=dumps({
            # TODO: Fix operation-id
            'type': 'resynchronize', 'operation-id': 1}))

def confirm_computer(modeladmin, request, queryset):
    queryset.update(confirmed=True)
    for comp in queryset:
        plugins = comp.company.activated_plugins.values_list('identifier', flat=True).order_by('identifier')
        Message.objects.create(computer=comp, message=dumps({
            'type': 'registration-done'}))

class ComputerAdmin(admin.ModelAdmin):
    actions = [force_resync, confirm_computer]
    exclude = ('confirmed', 'client_accepted_types', 'client_accepted_types_hash')

class CompanyAdmin(admin.ModelAdmin):
    exclude = ('activated_plugins_hash',)

    def save_model(self, request, obj, form, change):
        plugins = [i.identifier for i in form.cleaned_data['activated_plugins']]
        plugins.sort()
        obj.activated_plugins_hash = hash_types(plugins).encode('hex')
        obj.save()


admin.site.register(Computer, ComputerAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Message)
