# -*- coding: utf-8 -*-
import itertools
import logging
import operator
from pprint import pformat

from django.db import transaction
from django.db.models import F
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt

from landscape.lib.bpickle import loads

from mountain.core.models import Computer, Message
from mountain.core.utils import render_messages, MessageType, hash_types
from mountain.core.signals import message_available

message_logger = logging.getLogger('mountain.messaging')


@csrf_exempt
def ping(request):
    id = request.POST.get('insecure_id')
    msg_count = Message.objects.filter(computer__insecure_id=id).count()
    return render_messages(bool(msg_count), ping_answer=True)


@csrf_exempt
@transaction.commit_on_success
def message_system(request):
    secure_id = request.META.get('HTTP_X_COMPUTER_ID')
    data = loads(request.raw_post_data)
    received_msgs = data.pop('messages', [])

    if len(received_msgs) != data['total-messages']:
        raise

    return_msgs = []

    computer = company = None
    # Get company and computer objects if we do have a secure_id
    if secure_id:
        try:
            computer = Computer.objects.select_related('company')\
                                       .get(secure_id=secure_id)
            company = computer.company
            if not all((computer.next_client_sequence,
                        computer.next_server_sequence)):
                computer.next_client_sequence = data['sequence']
                computer.next_server_sequence = data['next-expected-sequence']
                computer.save()
        except Computer.DoesNotExist:
            return render_messages([{'type':'unkown-id'}])

    # Special case registration, as we could get a request with nothing,
    # and without accepting register, we'll never get a registration.
    if computer is not None and computer.confirmed:
        accepted_types = company.activated_plugins.values_list('identifier',
            flat=True).order_by('identifier')
        accepted_types_hash = company.activated_plugins_hash.decode('hex')
    else:
        accepted_types = ['register']
        accepted_types_hash = hash_types(['register'])

    # Check if sequence numbers match
    if computer is not None and computer.confirmed and \
       ((data['sequence'] != computer.next_client_sequence) or
       (data['next-expected-sequence'] != computer.next_server_sequence)):
            raise

    # Determine whether we need to notify the client about new/delete types
    if data.get('accepted-types') != accepted_types_hash:
        return_msgs.append({'type': 'accepted-types',
                            'types': list(accepted_types)})

    for msg in received_msgs:
        if computer is None and msg['type'] != 'register':
            continue

        message_logger.debug('Received message with data:\n%s' % pformat(msg))
        ret_ = message_available.send(sender=MessageType(msg['type']),
                                      computer=computer,
                                      request_data=data, msg_data=msg)
        ret = itertools.chain(*map(operator.itemgetter(1), ret_))

        return_msgs.extend(ret)

    messages = Message.objects.filter(computer=computer)
    if computer is not None:
        if messages.count():
            for msg in messages:
                return_msgs.append(simplejson.loads(msg.message))
            messages.delete()

        computer.next_client_sequence += data['total-messages']
        computer.next_server_sequence += len(return_msgs)
        # prevent sending of unneeded data
        Computer.objects.filter(pk=computer.pk).update(
            next_client_sequence = \
                F('next_client_sequence') + data['total-messages'],
            next_server_sequence = \
                F('next_server_sequence') + len(return_msgs))

    return render_messages(return_msgs, computer=computer)
