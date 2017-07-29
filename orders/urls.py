from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^create/$', views.order_create, name='order_create'),
    url(r'^created/$', views.order_created, name='order_created'),
    url(r'admin/order/(?P<order_id>\d+)/$', views.admin_order_detail, name='admin_order_detail'),
]