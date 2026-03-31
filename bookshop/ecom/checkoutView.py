from django.shortcuts import render, redirect,get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone


@login_required
def addToCart(req, slug):
    # phele product to find krna hoga
    book = get_object_or_404(Book, slug=slug)
    if book:
        # order check krna hoga ki user ka koi order chal rha h ya nhi jiska payment id null ho
        order_qs = Order.objects.filter(user_id=req.user, payment_id=None)
        if order_qs.exists():
            # order item check krna hoga ki order me ye book pehle se h ya nhi
            order = order_qs[0]
            order_item_qs = OrderItem.objects.filter(order_id=order, book_id=book)
            if order_item_qs.exists():
                # agr order item me ye book pehle se h to quantity ko 1 se badha do
                order_item = order_item_qs[0]
                order_item.quantity += 1
                order_item.save()
            else:
                # agr order item me ye book pehle se nhi h to order item create kr do
                OrderItem.objects.create(order_id=order, book_id=book, quantity=1)
        else:
            # agr order nhi h to order create kr do aur order item create kr do
            order = Order.objects.create(user_id=req.user, total_price=0)
            # order item create kr do
            OrderItem.objects.create(order_id=order, book_id=book, quantity=1)
    else:
        # agr book nhi mila to book view page pe redirect kr do
        return redirect("book_view", slug=slug)
    # agr book mil gaya to items order create or update ke baadd cart page pe redirect kr do
    return redirect("cart")

@login_required
def removeFromCart(req, slug):
    book = get_object_or_404(Book, slug=slug)
    if book:
        order_qs = Order.objects.filter(user_id=req.user, payment_id=None)
        if order_qs.exists():
            order = order_qs[0]
            order_item_qs = OrderItem.objects.filter(order_id=order, book_id=book)
            if order_item_qs.exists():
                order_item = order_item_qs[0]
                order_item.delete()
                return redirect("cart")
    else:
        return redirect("cart")

@login_required
def minusFromCart(req, slug):
    book = get_object_or_404(Book, slug=slug)
    if book:
        order_qs = Order.objects.filter(user_id=req.user, payment_id=None)
        if order_qs.exists():
            order = order_qs[0]
            order_item_qs = OrderItem.objects.filter(order_id=order, book_id=book)
            if order_item_qs.exists():
                order_item = order_item_qs[0]
                if order_item.quantity > 1:
                    order_item.quantity -= 1
                    order_item.save()
                else:
                    order_item.delete()
                return redirect("cart")
    else:
        return redirect("cart")
    

@login_required
def checkout(req):
    pass 

@login_required
def applyCoupon(req):
    if req.method == "POST":
        code = req.POST.get("code")
        # now check code
        print(timezone.now())
        coupon_qs = Coupon.objects.filter(code=code, active=True)
        if coupon_qs.exists():
            coupon = coupon_qs[0]
            # now check if user has an active order
            order_qs = Order.objects.filter(user_id=req.user, payment_id=None)
            if order_qs.exists():
                order = order_qs[0]
                order.coupon_id = coupon
                order.save()
                return redirect("cart")
            else:
                return redirect("cart") 
        else:
            # flash message that coupon is invalid
            return redirect("cart")
    else:
        return redirect("cart")

@login_required
def removeCoupon(req):
    order_qs = Order.objects.filter(user_id=req.user, payment_id=None)
    if order_qs.exists():
        order = order_qs[0]
        order.coupon_id = None
        order.save()
        return redirect("cart")
    else:
        return redirect("cart")
