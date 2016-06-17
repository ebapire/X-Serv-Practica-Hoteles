from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib import admindocs

urlpatterns = patterns('',

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$' , 'Hoteles.views.principal'),
    url(r'^alojamiento/(\d+)', 'Hoteles.views.alojamiento'),
    url(r'(\d+)', 'Hoteles.views.usuario'),
    url(r'^alojamientos$', 'Hoteles.views.alojamientos'),
    url(r'^about$', 'Hoteles.views.about'),
    url(r'^hoteles_filt$', 'Hoteles.views.hoteles_filt'),
    url(r'^login$','django.contrib.auth.views.login'),

)
