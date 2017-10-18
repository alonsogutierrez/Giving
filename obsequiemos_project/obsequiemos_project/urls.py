from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('obsequiemos.urls')),
    url(r'^/', include('social.apps.django_app.urls', namespace='social')),
]  # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG is True:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
