from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'shop'

urlpatterns = [
    path('', views.index, name='index'),
    path('flowers/', views.flower, name='flowers'),
    path('decorations', views.decoration, name='decorations'),
    path('cart/', views.view_cart, name='cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('add/', views.add_to_cart_bulk, name='add_to_cart_bulk'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
