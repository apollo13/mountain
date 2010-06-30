import uuid, string
from random import choice

from django.utils.simplejson import dumps

from mountain.core.models import Computer, Company
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

    comp,created = Computer.objects.get_or_create(
            hostname=msg_data['hostname'], company=company)
    comp.computer_title=msg_data['computer_title']
    comp.secure_id=  ''.join([choice(CHARS) for i in range(1600)])
    comp.insecure_id=str(uuid.uuid4())
    # TODO: this is only set on registration, but we need to check if the client changed them
    comp.client_accepted_types = dumps(request_data['client-accepted-types'])
    comp.client_accepted_types_hash = hash_types(request_data['client-accepted-types']).encode('hex')
    comp.save()


    return [{'type':'set-id', 'id':comp.secure_id,
             'insecure-id':comp.insecure_id}]

message_available.connect(handle_registration, sender=MessageType("register"))
