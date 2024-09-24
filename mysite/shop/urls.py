from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import add_to_cart

urlpatterns = [
    path('', views.index, name='index'),
    path('flowers/', views.flower, name='flowers'),
    path('decorations', views.decoration, name='decorations'),
    path('cart/', views.add_to_cart, name='cart'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
