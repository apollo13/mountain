from django.contrib import admin, messages
from django.utils.simplejson import dumps

from mountain.core.models import *
from mountain.core.utils import hash_types

def force_resync(modeladmin, request, queryset):
    for comp in queryset:
        Message.objects.create(computer=comp, message=dumps({
            # TODO: Fix operation-id
            'type': 'resynchronize', 'operation-id': 1}))
    messages.info(request, 'Queued resyncronisation for the selected computers.')

def confirm_computer(modeladmin, request, queryset):
    queryset.update(confirmed=True)
    for comp in queryset:
        plugins = comp.company.activated_plugins.values_list('identifier', flat=True).order_by('identifier')
        Message.objects.create(computer=comp, message=dumps({
            'type': 'registration-done'}))
    messages.info(request, 'Queued confirmation for the selected computers.')

def set_intervals(modelsamdin, request, queryset):
    for comp in queryset:
        Message.objects.create(computer=comp, message=dumps({
            'type': 'set-intervals',
            'ping': 10,
            'exchange': 30,
            'urgent-exchange': 10}))
    messages.info(request, 'Queued set-intervals for the selected computers.')

class ComputerAdmin(admin.ModelAdmin):
    actions = [force_resync, confirm_computer, set_intervals]
    exclude = ('client_accepted_types', 'client_accepted_types_hash')
    readonly_fields = ('confirmed',)

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
