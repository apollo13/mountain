import uuid, string
from random import choice

from django.utils.simplejson import dumps

from taggit.utils import parse_tags

from mountain.core.models import Computer, Company, Message
from mountain.core.signals import message_available
from mountain.core.utils import MessageType, hash_types

CHARS = string.ascii_letters + string.digits + string.punctuation

def handle_registration(sender, computer, request_data, msg_data, **kwargs):
    try:
        company = Company.objects.get(account_name=msg_data['account_name'])
    except Company.DoesNotExist:
       return [{'type':'registration', 'info':'unknown-account'}]

    if msg_data['registration_password'] != company.registration_password:
        return [{'type':'registration', 'info':'unknown-account'}]

    comp = Computer()
    comp.hostname=msg_data['hostname']
    comp.company=company
    comp.computer_title=msg_data['computer_title']
    comp.secure_id=  ''.join([choice(CHARS) for i in range(1600)])
    comp.insecure_id=str(uuid.uuid4())
    comp.client_accepted_types_hash = hash_types(request_data['client-accepted-types']).encode('hex')
    comp.save()
    comp.tags.set(*parse_tags(msg_data['tags']))

    return [{'type':'set-id', 'id':comp.secure_id,
             'insecure-id':comp.insecure_id}]

message_available.connect(handle_registration, sender=MessageType("register"))
