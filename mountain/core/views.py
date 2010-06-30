# -*- coding: utf-8 -*-
from django.utils import simplejson

from landscape.lib.bpickle import loads

from mountain.core.models import Computer, Message
from mountain.core.utils import render_messages, MessageType, hash_types
from mountain.core.signals import message_available

def ping(request):
    id = request.POST.get('insecure_id')
    msg_count = Message.objects.filter(computer__insecure_id=id).count()
    return render_messages(bool(msg_count), append_uuid=False)

def message_system(request):
    try:
        secure_id = request.META.get('HTTP_X_COMPUTER_ID')
        data = loads(request.raw_post_data)
        received_msgs = data.pop('messages', [])
        return_msgs = []

        computer = company = None
        # Get company and computer objects if we do have a secure_id
        if secure_id:
            try:
                computer = Computer.objects.get(secure_id=secure_id)
                company = computer.company
            except Computer.DoesNotExist:
                return render_messages({'type':'unkown-id'})

        # Special case registration, as we get a request with nothing,
        # and without accepting register, we'll never get a registration.
        if company:
            accepted_types = company.activated_plugins.values_list('identifier', flat=True).order_by('identifier')
            accepted_types_hash = company.activated_plugins_hash.decode('hex')
        else:
            accepted_types = ['register']
            accepted_types_hash = hash_types(['register'])

        # Determine whether we need to notify the client about new/delete types
        if data.get('accepted-types') != accepted_types_hash:
            return_msgs.append({'type':'accepted-types', 'types':list(accepted_types)})

        for msg in received_msgs:
            ret_ = message_available.send(sender=MessageType(msg['type']),
                                          computer=computer,
                                          request_data=data, msg_data=msg)
            ret_ = map(lambda x: x[1], ret_)
            ret = []
            for i in ret_:
                ret.extend(i if isinstance(i, (tuple,list)) else list(i))
            return_msgs.extend(ret)

        query = Message.objects.filter(computer=computer)
        if computer and query.count():
            messages = query
            for msg in messages:
                return_msgs.append(simplejson.loads(msg.message))
            query.delete()

    except Exception,e:
        import sys, traceback
        traceback.print_exception(*sys.exc_info())
        raise e

    return render_messages(return_msgs, computer=computer)
