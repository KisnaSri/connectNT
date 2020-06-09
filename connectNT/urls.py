from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from home import views


handler404 = 'home.views.error_404'
handler500 = 'home.views.error_500'

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('connectntadmin/', admin.site.urls),
    # path('administration/', admin.site.urls),
    path('', views.home, name='home'),
    path('', include('home.urls', namespace='home')),
    # path('registration/', include('registration.urls', namespace='registration')),
    path('ckeditor/', include('ckeditor_uploader.urls'))
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)