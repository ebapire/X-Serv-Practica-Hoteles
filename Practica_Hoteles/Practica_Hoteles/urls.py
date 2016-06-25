from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib import auth
from django.contrib import admindocs
from django.conf import settings

urlpatterns = patterns('',

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$' , 'Hoteles.views.principal'),
    url(r'^alojamiento/(\d+)/idioma', 'Hoteles.views.idioma'),
    url(r'^actividad/css/(?P<path>.*)$', 'django.views.static.serve', {'document_root' : settings.STATIC_URL2}),
    url(r'^alojamiento/(\d+)', 'Hoteles.views.alojamiento'),
    url(r'^(\d+)/xml', 'Hoteles.views.user_xml'),
    url(r'(\d+)', 'Hoteles.views.usuario'),
    url(r'^alojamientos$', 'Hoteles.views.alojamientos'),
    url(r'^about$', 'Hoteles.views.about'),
    url(r'^hoteles_filt$', 'Hoteles.views.hoteles_filt'),
    url(r'^login$','django.contrib.auth.views.login'),
    url(r'^logout$','django.contrib.auth.views.logout'),
    url(r'^accounts/profile/', 'Hoteles.views.principal'),
    url(r'^anadir_css', 'Hoteles.views.anadir_css'),
    url(r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root' : settings.STATIC_URL2}),


)
