from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
from .forms import ShippingForm, CreateUserForm
from .utils import return_session, return_order_and_items
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .decorators import if_unauthenticated


def store(request):
    order, items = return_order_and_items(request)
    products = Product.objects.all()
    context = {'products': products, 'items': items, 'order': order}
    return render(request, 'store/store.html', context)


def cart(request):
    order, items = return_order_and_items(request)
    context = {'items': items, 'order': order}
    return render(request, 'store/cart.html', context)


def checkout(request):
    order, items = return_order_and_items(request)
    shipping_form = ShippingForm()
    context = {'items': items, 'order': order, 'shipping_form': shipping_form}
    return render(request, 'store/checkout.html', context)


@csrf_exempt
def update_cart(request):
    if request.POST:
        try:
            product_id = request.POST['id']
            action = request.POST['action']

            # if request.user.is_authenticated:
            #     customer = request.user.customer
            # else:
            #     session_key = return_session(request)
            #     customer, created = Customer.objects.get_or_create(as_guest=session_key)
            order, items = return_order_and_items(request)

            try:
                product = Product.objects.get(id=product_id)
            except ObjectDoesNotExist:
                return JsonResponse(status=422, data={'error': 'you must provide valid id'})

            # order, created = Order.objects.get_or_create(customer=customer, complete=False)

            order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

            if action == 'add':
                order_item.quantity += 1
            elif action == 'remove':
                order_item.quantity -= 1
            else:
                return JsonResponse(status=422, data={'error': 'you must provide valid action'})

            order_item.save()

            if order_item.quantity <= 0:
                order_item.delete()

            return JsonResponse('item added', safe=False)
        except KeyError:
            return JsonResponse(status=400, data={'error': 'you must provide id and action'})

    return JsonResponse(status=405, data={'error': 'you must provide post request'})


def validate_form(request):
    if request.method == "POST":
        form = ShippingForm(request.POST)

        if request.user.is_authenticated:
            customer = request.user.customer
        else:
            session_key = return_session(request)
            customer, created = Customer.objects.get_or_create(as_guest=session_key)

            if request.POST.get('name'):
                name = request.POST.get('name')
                customer.name = name

            if request.POST.get('email'):
                email = request.POST.get('email')
                email_query = User.objects.filter(email=email)
                if email_query:
                    return JsonResponse(status=400, data={'error': 'This email is already occupied, try another'})
                customer.email = email

            # print('Creating or updating new Customer with')
            customer.save()

        order = customer.order_set.get(customer=customer)

        if order.shipping:
            if form.is_valid():
                address = request.POST.get('address')
                city = request.POST.get('city')
                phone = request.POST.get('phone')

                update = {'address': address, 'city': city, 'phone': phone}

                ShippingAddress.objects.update_or_create(customer=customer, order=order, defaults=update)

                return JsonResponse('ok', safe=False, status=200)
            else:
                return JsonResponse(status=400, data={'error': 'You must provide shipping address'})

        return JsonResponse(status=200, data={'ok': 'ok'})

    return JsonResponse(status=405, data={'error': 'you must provide post request'})


def completed_order(request):
    """
    Future improvements: when payment methods are added, make query with paid=True, and change get_or_create on
    just get(). Moreover take transaction ID from payment widget and write it into DB.
    :param request:
    :return: render template
    """
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        session_key = return_session(request)
        customer, created = Customer.objects.get_or_create(as_guest=session_key)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()

    # order.transaction_id = take_this_from_payment_response
    order.complete = True
    order.save()

    context = {'items': items, 'order': order}
    return render(request, 'store/order.html', context)


def completed_orders(request):
    if request.user.is_authenticated:
        customer = request.user.customer
    else:
        session_key = return_session(request)
        customer, created = Customer.objects.get_or_create(as_guest=session_key)

    orders = Order.objects.filter(customer=customer)

    context = {'orders': orders}
    return render(request, 'store/orders.html', context)


@if_unauthenticated
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('store')
        else:
            return render(request, 'store/login.html', {'error': 'Incorrect login/password, try again.'})

    context = {}
    return render(request, 'store/login.html', context)


@if_unauthenticated
def registration_view(request):
    # print('registration_view', request.POST)

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Account was created successfully, now you can log in.')
            return redirect('login')
        else:
            return JsonResponse(status=400, data={'error': 'You must provide valid data'})

    context = {'form': form}
    return render(request, 'store/registration.html', context)


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    context = {}
    return redirect('login')


