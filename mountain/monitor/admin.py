from django.contrib import admin

from mountain.monitor.models import ComputerInfo#, ProcessorInfo, HardwarePart

class ProcessorInfoAdmin(admin.ModelAdmin):
    list_display = ('model', 'vendor', 'processor_id', 'cache_size', 'computer')
    list_filter = ('computer',)

class HardwarePartAdmin(admin.ModelAdmin):
    list_display = ('product', 'vendor', 'computer')
    list_filter = ('computer',)

class ComputerInfoAdmin(admin.ModelAdmin):
    list_display = ('hostname', 'code_name', 'description', 'distributor_id', 'release', 'computer')

#admin.site.register(ProcessorInfo, ProcessorInfoAdmin)
#admin.site.register(HardwarePart, HardwarePartAdmin)
admin.site.register(ComputerInfo, ComputerInfoAdmin)
