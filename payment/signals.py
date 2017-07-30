from django.shortcuts import get_object_or_404
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received
from django.dispatch import receiver
from orders.models import Order

@receiver(valid_ipn_received)
@receiver(invalid_ipn_received)
def payment_notification(sender, **kwargs):
    ipn_obj = sender
    order = get_object_or_404(Order, id=ipn_obj.invoice)
    print(sender)
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # Payment is successful
        order.paid = True
        order.save()