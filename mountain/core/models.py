from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from taggit.managers import TaggableManager

class AcceptedTypes(models.Model):
    """This models holds the message types which are supported by this server.
    They are selectable through the company model, so each customer can
    suppport different types (eg. not everyone needs a hardware inventory)
    """
    identifier = models.CharField(max_length=255)

    def __unicode__(self):
        return self.identifier

class Company(models.Model):
    """Company is used to define administrator and the activated plugins.
    """
    verbose_name = models.CharField(_('verbose name'), max_length=255)
    account_name = models.CharField(_('account name'), max_length=255, unique=True)
    registration_password = models.CharField(_('registration password'), max_length=255)
    administratos = models.ManyToManyField(User, verbose_name=_('administrators'))
    activated_plugins = models.ManyToManyField(AcceptedTypes, verbose_name=_('activated plugins'))
    activated_plugins_hash = models.CharField(max_length=255)

    def __unicode__(self):
        return self.verbose_name

    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')

class Computer(models.Model):
    """Represents one Computer, information is pulled from the client
    registration request. Secure id is used to identify the computer,
    if someone can sniff this id, he __will__ be able to connect as
    this computer.
    """
    company = models.ForeignKey(Company, verbose_name=_('company'))
    computer_title = models.CharField(_('computer title'), max_length=255)
    hostname = models.CharField(_('hostname'), max_length=255, unique=True)
    # TODO: uniqness of secureid
    secure_id = models.TextField(_('secure id'))
    insecure_id = models.CharField(_('insecure id'), max_length=36, unique=True)
    client_accepted_types_hash = models.CharField(max_length=255)
    confirmed = models.BooleanField(_('confirmed'), default=False)

    next_client_sequence = models.IntegerField(null=True, blank=True)
    next_server_sequence = models.IntegerField(null=True, blank=True)

    tags = TaggableManager()

    def __unicode__(self):
        return self.computer_title

    class Meta:
        verbose_name = _('Computer')
        verbose_name_plural = _('Computers')
        unique_together = ('company', 'computer_title')

class Message(models.Model):
    """Message which is queued and should get send to the client"""
    computer = models.ForeignKey(Computer, verbose_name=_('computer'))
    message = models.TextField(_('message'), help_text=_('JSON encoded'))

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')


