from django.urls import path
from .views import store, cart, checkout, addItem, removeItem

urlpatterns = [
    path('', store.as_view(), name='store'),
    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('add_item/<int:pk>/', addItem, name='add_item'),
    path('remove_item/<int:pk>/', removeItem, name='remove_item'),
]
