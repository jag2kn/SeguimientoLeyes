from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'seguimiento.views.home', name='home'),
    
    url(r'^proyectos/lista/$', 'seguimiento.proyecto.lista'),
    url(r'^proyecto/(?P<proyecto_id>\d+)/$', 'seguimiento.proyecto.detalle'),
    
    # url(r'^leyes/', include('leyes.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
