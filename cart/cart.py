from decimal import Decimal
from django.conf import settings
from shop.models import Product
from coupons.models import Coupon

class Cart(object):
    def __init__(self, request):
        # Initialize Cart
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            # save an empty cart in session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        self.coupon_id = self.session.get('coupon_id')


    def __iter__(self):
        # Iterate over the items in the cart and get the products from database
        product_ids = [id.split("_")[0] for id in self.cart.keys()]

        products = Product.objects.filter(id__in=product_ids)
        for key in self.cart.keys():
            cart_item_id = key.split("_")[0]
            self.cart[key]['product'] = products.get(id=cart_item_id)

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        # Count of all items in the cart
        return sum(item['quantity'] for item in self.cart.values())

    @property
    def coupon(self):
        if self.coupon_id:
            return Coupon.objects.get(id=self.coupon_id)
        return None

    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal('100') * self.get_total_price())
        return Decimal('0')

    def add(self, product, size, quantity=1, update_quantity=False):
        # add product to the cart along with quantity
        product_id = "{}_{}".format(product.id, size)
        if product_id not in self.cart:
            self.cart[product_id] = {'size':size, 'quantity':0, 'price': str(product.price)}

        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def remove(self, product, size):
        # remove a product from the cart
        product_id = "{}_{}".format(product.id, size)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        # update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def get_total_price(self):
        # return the total price of all items
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()

    def clear(self):
        # remove current cart from session
        del self.session[settings.CART_SESSION_ID]
        self.session['coupon_id'] = None
        self.session.modified = True
