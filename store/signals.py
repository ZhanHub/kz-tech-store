from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Order

@receiver(post_delete, sender=Order)
def update_stock_after_order_delete(sender, instance, **kwargs):
    product = instance.product
    if product:
        product.stock += instance.quantity
        product.save()
