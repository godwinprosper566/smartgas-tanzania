from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Order


def home(request):
    pending_count = Order.objects.filter(status='Pending').count()
    total_orders = Order.objects.count()
    total_sales = sum(order.price for order in Order.objects.all())

    return render(request, 'orders/home.html', {
        'pending_count': pending_count,
        'total_orders': total_orders,
        'total_sales': total_sales,
    })


def order_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        location = request.POST.get('location')
        customer_type = request.POST.get('customer_type')
        size_kg = int(request.POST.get('size_kg'))
        notes = request.POST.get('notes', '')

        if customer_type == 'Vehicle':
            price_per_kg = 2800
        else:
            price_per_kg = 3200

        price = size_kg * price_per_kg

        new_order = Order.objects.create(
            name=name,
            phone=phone,
            location=location,
            customer_type=customer_type,
            size_kg=size_kg,
            price=price,
            status='Pending',
            payment_status='Unpaid',
            notes=notes
        )
        return redirect('success', order_id=new_order.id)

    return render(request, 'orders/order.html')


def success(request, order_id):
    return render(request, 'orders/success.html', {
        'order_id': order_id
    })


@login_required(login_url='login')
def order_list(request):
    status_filter = request.GET.get('status')
    customer_type = request.GET.get('type')
    payment_filter = request.GET.get('payment')
    search = request.GET.get('q', '').strip()

    orders = Order.objects.all().order_by('-id')

    if status_filter in ['Pending', 'Out for Delivery', 'Delivered']:
        orders = orders.filter(status=status_filter)

    if customer_type in ['Household', 'Vehicle', 'Business']:
        orders = orders.filter(customer_type=customer_type)

    if payment_filter in ['Paid', 'Unpaid']:
        orders = orders.filter(payment_status=payment_filter)

    if search:
        orders = orders.filter(name__icontains=search) | orders.filter(phone__icontains=search)

    total_sales = sum(order.price for order in orders)
    pending_count = Order.objects.filter(status='Pending').count()

    return render(request, 'orders/order_list.html', {
        'orders': orders,
        'total_sales': total_sales,
        'pending_count': pending_count,
        'search': search,
    })


@login_required(login_url='login')
def mark_delivered(request, order_id):
    order = Order.objects.get(id=order_id)
    order.status = 'Delivered'
    order.save()
    messages.success(request, f"Order #{order_id} marked as Delivered.")
    return redirect('order_list')


@login_required(login_url='login')
def mark_out_for_delivery(request, order_id):
    order = Order.objects.get(id=order_id)
    order.status = 'Out for Delivery'
    order.save()
    messages.success(request, f"Order #{order_id} is now Out for Delivery.")
    return redirect('order_list')


@login_required(login_url='login')
def mark_paid(request, order_id):
    order = Order.objects.get(id=order_id)
    order.payment_status = 'Paid'
    order.save()
    messages.success(request, f"Order #{order_id} marked as Paid.")
    return redirect('order_list')


@login_required(login_url='login')
def delete_order(request, order_id):
    order = Order.objects.get(id=order_id)
    order.delete()
    messages.success(request, f"Order #{order_id} has been deleted.")
    return redirect('order_list')


@login_required(login_url='login')
def edit_order(request, order_id):
    order = Order.objects.get(id=order_id)

    if request.method == 'POST':
        order.name = request.POST.get('name')
        order.phone = request.POST.get('phone')
        order.location = request.POST.get('location')
        order.customer_type = request.POST.get('customer_type')
        order.size_kg = int(request.POST.get('size_kg'))
        order.status = request.POST.get('status')
        order.payment_status = request.POST.get('payment_status')
        order.notes = request.POST.get('notes', '')

        if order.customer_type == 'Vehicle':
            price_per_kg = 2800
        else:
            price_per_kg = 3200

        order.price = order.size_kg * price_per_kg
        order.save()
        messages.success(request, f"Order #{order_id} updated successfully.")
        return redirect('order_list')

    return render(request, 'orders/edit_order.html', {
        'order': order
    })


@login_required(login_url='login')
def daily_report(request):
    today = timezone.now().date()
    orders = Order.objects.filter(created_at__date=today).order_by('-id')
    total_sales = sum(order.price for order in orders)
    total_orders = orders.count()

    return render(request, 'orders/daily_report.html', {
        'orders': orders,
        'total_sales': total_sales,
        'total_orders': total_orders,
        'today': today,
    })


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'orders/login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'orders/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


def track_order(request):
    order = None
    error = None

    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            error = "Order not found. Please check the Order ID."

    return render(request, 'orders/track_order.html', {
        'order': order,
        'error': error
    })


@login_required(login_url='login')
def dashboard(request):
    total_orders = Order.objects.count()
    pending = Order.objects.filter(status='Pending').count()
    out_for_delivery = Order.objects.filter(status='Out for Delivery').count()
    delivered = Order.objects.filter(status='Delivered').count()
    paid = Order.objects.filter(payment_status='Paid').count()
    unpaid = Order.objects.filter(payment_status='Unpaid').count()
    total_sales = sum(order.price for order in Order.objects.all())
    today_orders = Order.objects.filter(created_at__date=timezone.now().date()).count()
    recent_orders = Order.objects.all().order_by('-id')[:5]

    return render(request, 'orders/dashboard.html', {
        'total_orders': total_orders,
        'pending': pending,
        'out_for_delivery': out_for_delivery,
        'delivered': delivered,
        'paid': paid,
        'unpaid': unpaid,
        'total_sales': total_sales,
        'today_orders': today_orders,
        'recent_orders': recent_orders,
    })