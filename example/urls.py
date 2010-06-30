from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import mountain.core.urls

urlpatterns = patterns('',
    # Example:
    # (r'^example/', include('example.foo.urls')),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    (r'^', include(mountain.core.urls))
)
