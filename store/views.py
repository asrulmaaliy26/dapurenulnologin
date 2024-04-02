from django.contrib.sessions.models import Session
from django.utils import timezone
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render
from django.contrib import messages

from .models import *

class store(View):
    def get(self, request):
        products = Product.objects.all()

        # Mendapatkan jumlah item dalam keranjang belanja dari session
        cart_items = request.session.get('cart', [])
        total_quantity = sum(item['quantity'] for item in cart_items)

        context = {
            "products": products,
            "num_items_in_cart": total_quantity,  # Menambahkan jumlah item dalam keranjang belanja ke dalam konteks
        }
        session_data = request.session.items()
        return render(request, "store/store.html", context)

def cart(request):
    # Mengambil daftar item dari session
    items = request.session.get('cart', [])
    
    # Menghitung total harga
    total_price_full = sum(item['price'] * item['quantity'] for item in items)
    
    # Memasukkan total harga ke dalam setiap item dan menamainya sebagai total_price
    for item in items:
        item['total_price'] = item['price'] * item['quantity']

    # Membuat konteks untuk dikirim ke template
    context = {
        "items": items,
        "total_price_full": total_price_full,
    }
    
    return render(request, "store/cart.html", context)

@csrf_exempt
def checkout(request):
    cart_items = request.session.get('cart', [])
    
    # Menghitung total quantity
    total_quantity = sum(item['quantity'] for item in cart_items)
    
    # Menghitung total harga
    total_price = sum(item['price'] * item['quantity'] for item in cart_items)
    
    # Simulate completing the order (since we're not using a database)
    request.session['cart'] = []  # Clear the cart after checkout
    
    messages.success(request, "Your order has been successfully completed!")
    
    context = {
        "items": cart_items,
        "total_price": total_price,
        "total_quantity": total_quantity,  # Menambahkan total quantity ke dalam konteks
    }
    return render(request, "store/checkout.html", context)

def addItem(request, pk):
    try:
        product = Product.objects.get(id=pk)
        
        # Inisialisasi keranjang belanja jika belum ada
        if 'cart' not in request.session:
            request.session['cart'] = []

        # Cek apakah produk sudah ada di keranjang belanja
        cart_items = request.session['cart']
        item_exists = False
        for item in cart_items:
            if item['product_id'] == pk:
                item['quantity'] += 1
                item_exists = True
                break

        # Jika produk belum ada di keranjang belanja, tambahkan produk baru
        if not item_exists:
            cart_items.append({
                'product_id': pk,
                'name': product.name,
                'price': product.price,
                'quantity': 1,
            })

        # Simpan keranjang belanja dalam session
        request.session['cart'] = cart_items

        messages.success(request, "Your item is successfully added!")
    except Product.DoesNotExist:
        messages.error(request, "Product does not exist!")

    return redirect("store")


def removeItem(request, pk):
    # Pastikan 'cart' ada dalam session
    if 'cart' in request.session:
        cart_items = request.session['cart']

        # Cari item yang akan dihapus dari keranjang belanja
        for item in cart_items:
            if item['product_id'] == pk:
                # Hapus item dari keranjang belanja
                cart_items.remove(item)
                request.session['cart'] = cart_items
                messages.success(request, "Item removed successfully!")
                break
    return redirect("cart")