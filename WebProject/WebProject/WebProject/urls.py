"""
Definition of urls for WebProject.
"""

from datetime import datetime

import django.contrib.auth.views
from django.conf.urls import url

#Импорт библиотек для медиа файлов
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin

from WebProject.settings import DEBUG

urlpatterns = [
    # Examples:
    url(r'^', include('webshop.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)		#url для медиа файлов

if DEBUG:
    import debug_toolbar
    urlpatterns = [
        
        url(r'^__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns