from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, WrappingPaper, Products, Decorations
from django.db.models.signals import post_save


@receiver(post_save, sender=Products)
def update_product_remaining(sender, instance, created, **kwargs):
    if created:
        product = instance.roses
        product.update_remaining(instance.roses_qty)


@receiver(post_save, sender=Order)
def update_decorations_remaining(sender, instance, created, **kwargs):
    if created:
        decoration = instance.decoration
        decoration.update_remaining(instance.decoration_qty)


@receiver(post_save, sender=Order)
def update_wp_remaining(sender, instance, created, **kwargs):
    if created:
        wrapping_paper = instance.wrappingpaper
        wrapping_paper.update_remaining(instance.wp_qty)

