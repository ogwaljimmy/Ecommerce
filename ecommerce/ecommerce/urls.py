from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin url
    path('admin/', admin.site.urls),

    # App URLs
    path('', include('store.urls')),
    path('cart/', include('cart.urls')),
    path('account/', include('account.urls')),
    path('payment/', include('payment.urls')),
    path('', include('pwa.urls')),  # PWA must not conflict with root views
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
