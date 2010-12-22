from django.db import models

from mountain.core.models import Computer

#class ProcessorInfo(models.Model):
#    computer = models.ForeignKey(Computer)
#    processor_id = models.SmallIntegerField()
#    model = models.CharField(max_length=255)
#
#    vendor = models.CharField(max_length=255, default='')
#    cache_size = models.SmallIntegerField(null=True)
#
#    def __unicode__(self):
#        return self.model
#
#class HardwarePart(models.Model):
#    computer = models.ForeignKey(Computer)
#    udi = models.CharField(max_length=255)
#    product = models.CharField(max_length=255)
#    vendor = models.CharField(max_length=255, default='')
#    driver = models.CharField(max_length=255, default='')
#    subsystem = models.CharField(max_length=255, default='')
#
#    def __unicode__(self):
#        return self.product

class ComputerInfo(models.Model):
    computer = models.ForeignKey(Computer)
    hostname = models.CharField(max_length=255)
    code_name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    distributor_id = models.CharField(max_length=255)
    release = models.CharField(max_length=255)
    total_memory = models.IntegerField(default=0)
    total_swap = models.IntegerField(default=0)
