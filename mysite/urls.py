from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('users.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('blog.urls')),
    path('polls/', include('polls.urls'))
]

if settings.DEBUG: urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)