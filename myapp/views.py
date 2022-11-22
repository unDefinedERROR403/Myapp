from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Category, Product, Client, Order
from django.shortcuts import get_object_or_404
from .forms import OrderForm, InterestForm, NewUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages


# Create your views here.

def index(request):
    cat_list = Category.objects.all().order_by('id')[:10]
    msg = ""
    last_login = "You are logged out"
    if request.session.get('last_login', False):
        last_login = datetime.strptime(request.session.get('last_login'), "%Y-%m-%d %H:%M:%S.%f")
        time = datetime.now() - last_login
        if time.total_seconds() > 3600:
            msg = "Your last login was more than one hour ago"
            logout(request)
    context = {
        'cat_list': cat_list,
        'last_login': last_login,
        'user': request.user
    }
    return render(request, 'myapp/index.html', context=context)


def about(request):
    if 'about_visits' in request.COOKIES:
        count_visited = int(request.COOKIES['about_visits'])
        response = render(request, 'myapp/about.html', {'no_of_times_visited': count_visited + 1})
        response.set_cookie('about_visits', count_visited + 1, max_age=300)
    else:
        response = render(request, 'myapp/about.html', {'no_of_times_visited': 1})
        response.set_cookie('about_visits', 1)
    return response


def detail(request, cat_no):
    category = get_object_or_404(Category, pk=cat_no)
    products = Product.objects.filter(category=category)
    return render(request, 'myapp/detail.html', {'category': category, 'products': products})


def products(request):
    prodlist = Product.objects.all().order_by('id')[:10]
    return render(request, 'myapp/products.html', {'prodlist': prodlist})


@login_required
def place_order(request):
    msg = ''
    prodlist = Product.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            product_name = form.cleaned_data['product']
            order = form.save(commit=False)
            if order.num_units <= order.product.stock:
                order.save()
                product = Product.objects.get(name=product_name)
                product.stock = product.stock - order.num_units
                product.save()
                msg = 'Your order has been placed successfully.'
            else:
                msg = 'We do not have sufficient stock to fill your order !!!'
                return render(request, 'myapp/order_response.html', {'msg': msg})
    else:
        form = OrderForm()
    return render(request, 'myapp/placeorder.html', {'form': form, 'msg': msg, 'prodlist': prodlist})


def productdetail(request, prod_id):
    try:
        msg = ''
        product = Product.objects.get(id=prod_id)
        # product = get_object_or_404(Product, pk=prod_id)
        if request.method == 'GET':
            form = InterestForm()
        elif request.method == 'POST':
            form = InterestForm(request.POST)
            if form.is_valid():
                interested = form.cleaned_data['interested']
                print("Interested: ", interested)
                if int(interested) == 1:
                    product.interested += 1
                    product.save()
                    print('form is valid')
                    return redirect(reverse('myapp:index'))
        return render(request, 'myapp/productdetail.html', {'form': form, 'msg': msg, 'product': product})
    except Product.DoesNotExist:
        msg = 'The requested product does not exist. Please provide correct product id !!!'
        return render(request, 'myapp/productdetail.html', {'msg': msg})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                cur_datetime = datetime.now()
                request.session['last_login'] = str(cur_datetime)
                request.session.set_expiry(3600)
                return HttpResponseRedirect(reverse('myapp:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('myapp:index'))


@login_required
def myorders(request):
    try:
        user = request.user
        print(user)
        client = Client.objects.get(username=user.username)
        orders = Order.objects.filter(client=client)
        msg = f'Orders placed by {client} :-'
        if orders.count() == 0:
            msg = 'Client has not placed any orders'
        return render(request, 'myapp/myorders.html', {'orders': orders, 'msg': msg})
    except Client.DoesNotExist:
        msg = 'You are not a registered client'
        return render(request, 'myapp/myorders.html', {'msg': msg})


def register(request):
    msg1 = f'Registration Status: Ongoing'
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg1 = 'Registration Successful. Login to continue shopping...'
            return render(request, "myapp/register.html", {'msg': msg1})
        msg1 = 'Unsuccessful registration. Invalid information.'
    form = NewUserForm()
    return render(request, "myapp/register.html", {"register_form": form, 'msg': msg1})
