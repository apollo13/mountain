from hashlib import md5

from landscape.lib.bpickle import dumps

from django.http import HttpResponse

from mountain.core.settings import SERVER_UUID
from mountain.core.models import AcceptedTypes

def render_messages(messages, computer=None, append_uuid=True):
    """Updates the answer with the server-uuid, pickles it and returns the
    HttpReponse.
    """
    ret = {'messages': messages}
    if append_uuid:
        ret.update({'server-uuid': SERVER_UUID})
    if computer:
        ret.update({'client-accepted-types-hash': computer.client_accepted_types_hash.decode('hex')})
    return HttpResponse(dumps(ret))

def MessageType(type, __instance_cache={}):
    """Use this to register your receiver function to a string.
    """
    instance = __instance_cache.setdefault(type, object())
    return instance

def hash_types(types):
    """The client only sends the hashed server types, we do the same,
    compare them and only send new types if the types difer.
    """
    m = md5()
    m.update(";".join(types))
    return m.digest()

def register_messagetype(type):
    from django.db.models.signals import post_syncdb
    from mountain.core import models

    def install_type(sender, app, created_models, verbosity=0, **kwargs):
        if verbosity>=1:
            print "Installing message type %s" % type
            AcceptedTypes.objects.get_or_create(identifier=type)

    post_syncdb.connect(install_type, sender=models, weak=False)

