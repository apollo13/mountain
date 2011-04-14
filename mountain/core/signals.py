import django.dispatch

message_available = django.dispatch.Signal(providing_args=['computer',
    'request_data', 'msg_data'])
