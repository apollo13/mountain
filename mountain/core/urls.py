from django.conf.urls.defaults import *

from views import message_system, ping

urlpatterns = patterns('',
    (r'message-system/?$', message_system),
    (r'ping/?$', ping),
)
