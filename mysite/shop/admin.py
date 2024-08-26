from django.contrib import admin
from .models import Products, Decorations, WrappingPaper, Order, Client, PhoneModel, UploadedImage

# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    list_display = ('client', 'roses', 'roses_qty', 'decoration', 'decoration_qty',  'wrappingpaper', 'wp_qty', 'get_total')

    def get_total(self, obj):
        return obj.total()
    get_total.short_description = 'Total'


class ProductsAdmin(admin.ModelAdmin):
    list_display = ('color', 'remaining', 'price', 'image', 'image_upload')


class DecorationAdmin(admin.ModelAdmin):
    list_display = ('type', 'remaining', 'price')


class WrappingPaperAdmin(admin.ModelAdmin):
    list_display = ('color', 'remaining')


class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'client_phone_number', 'email')


class PhoneModelAdmin(admin.ModelAdmin):
    list_display = ('phone_number', )


@admin.register(UploadedImage)
class UploadedImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'image')


admin.site.register(Products, ProductsAdmin)
admin.site.register(Decorations, DecorationAdmin)
admin.site.register(WrappingPaper, WrappingPaperAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(PhoneModel, PhoneModelAdmin)

