from django.db import models

from mountain.core.models import Computer

class PackageHashManager(models.Manager):
    def hashes_in_bulk(self, id_list):
        qs = self.model.objects.filter(hash__in=id_list)
        return dict((obj.hash, obj) for obj in qs.iterator())

class PackageHash(models.Model):
    hash = models.CharField(max_length=40, db_index=True, unique=True)
    name = models.CharField(max_length=255)
    summary = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    description = models.TextField()
    installed_size = models.IntegerField(null=True)
    size = models.IntegerField()
    type = models.IntegerField()
    section = models.CharField(max_length=255)

    objects = PackageHashManager()

    class Meta:
        verbose_name = "Package hash"
        verbose_name_plural = "Package hashes"
