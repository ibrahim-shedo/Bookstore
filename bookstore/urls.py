from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from dashboard.views import mark_messages_as_read


urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls')),
    path('search/', include('search.urls')),
    path('order/', include('order.urls')),
    path('',include("store.urls")),
    path('dashboard/',include("dashboard.urls")),
    path('mark_messages_as_read/', mark_messages_as_read, name='mark_messages_as_read'),



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
