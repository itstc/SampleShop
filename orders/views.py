from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from .models import Order, OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart

from .tasks import order_created

# Create your views here.

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'],
                                         price=item['price'], size=item['size'], quantity=item['quantity'])
            #order_created.delay(order.id)
            cart.clear()
            request.session['order_id'] = order.id
            return HttpResponseRedirect(reverse("payment:process"))
    else:
        form = OrderCreateForm()
        
    return render(request, 'orders/order/create.html', {'cart':cart, 'form':form})

def order_created(request):
    return render(request, 'orders/order/created.html')

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order':order})