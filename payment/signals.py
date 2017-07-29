from django.shortcuts import get_object_or_404
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from orders.models import Order

def payment_notification(sender, **kwargs):
    ipn_obj = sender
    order = get_object_or_404(Order, id=ipn_obj.invoice)
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # Payment is successful
        order.paid = True
        order.save()
    else:
        # Payment is canceled
        order.delete()

    valid_ipn_received.connect(payment_notification)