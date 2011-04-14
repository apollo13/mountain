from django.db import models

from landscape.package import skeleton

from mountain.core.models import Computer


TYPE_CHOICES = (
    (skeleton.DEB_PACKAGE, 'Package'),
    (skeleton.DEB_PROVIDES, 'Provides'),
    (skeleton.DEB_NAME_PROVIDES, 'Name provides'),
    (skeleton.DEB_REQUIRES, 'Requires'),
    (skeleton.DEB_OR_REQUIRES, 'Or Requires'),
    (skeleton.DEB_UPGRADES, 'Upgrades'),
    (skeleton.DEB_CONFLICTS, 'Conflicts'),
)

STATUS_CHOICES = (
    (0, 'installed'),
    (1, 'available'),
    (2, 'available-upgrades'),
    (3, 'locked'),
)

class PackageManager(models.Manager):
    def hashes_in_bulk(self, id_list):
        qs = self.model.objects.filter(hash__in=id_list)
        return dict((obj.hash, obj) for obj in qs.iterator())


class Package(models.Model):
    hash = models.CharField(max_length=40, db_index=True, unique=True)
    name = models.CharField(max_length=255)
    summary = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    description = models.TextField()
    installed_size = models.IntegerField(null=True)
    size = models.IntegerField()
    type = models.IntegerField(choices=TYPE_CHOICES)
    section = models.CharField(max_length=255)

    objects = PackageManager()

    class Meta:
        verbose_name = 'Package'
        verbose_name_plural = 'Packages'


class PackageRelation(models.Model):
    package = models.ForeignKey(Package)
    type = models.IntegerField(choices=TYPE_CHOICES)
    target = models.TextField()


class PackageStatus(models.Model):
    computer = models.ForeignKey(Computer)
    package = models.ForeignKey(Package)
    status = models.IntegerField(choices=STATUS_CHOICES)
