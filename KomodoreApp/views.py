from django.contrib.auth import authenticate, login
from django.db.models import F, Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from KomodoreApp.forms import RegistrationForm, LoginForm, AddProductForm
from KomodoreApp.models import Profile, Car, Product, ShoppingCart


# Create your views here.
def buyer_registration(request):
    context = {"form": RegistrationForm()}
    if request.method == "POST":
        form_data = RegistrationForm(data=request.POST, files=request.FILES)
        if form_data.is_valid():
            user = form_data.save(commit=False)
            password = form_data.cleaned_data.get('password1')
            user.set_password(password)
            user.save()
            user = authenticate(username=user.username, password=password)
            login_view(request, user)
            profile = Profile()
            profile.user = user
            profile.is_buyer = True
            profile.is_seller = False
            profile.save()
            shopping_cart = ShoppingCart(user=user)
            shopping_cart.save()
            return redirect("home")

    return render(request, "buyer_registration.html", context=context)


def seller_registration(request):
    context = {"form": RegistrationForm()}

    if request.method == "POST":
        form_data = RegistrationForm(data=request.POST, files=request.FILES)
        if form_data.is_valid():
            user = form_data.save(commit=False)
            password = form_data.cleaned_data.get('password1')
            user.set_password(password)
            user.save()
            user = authenticate(username=user.username, password=password)
            login_view(request, user)
            profile = Profile()
            profile.user = user
            profile.is_buyer = False
            profile.is_seller = True
            profile.save()

            return redirect("home")
    return render(request, "seller_registration.html", context=context)


def login_view(request):
    context = {"form": LoginForm()}

    if request.method == "POST":
        form_data = LoginForm(data=request.POST, files=request.FILES)
        if form_data.is_valid():
            username = form_data.cleaned_data.get('username')
            password = form_data.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                pass
    return render(request, "login.html", context=context)


def home(request):
    if not request.user.is_authenticated:
        return redirect("/login/")
    profile = Profile.objects.get(user=request.user)
    context = {"is_buyer": profile.is_buyer, "is_seller": profile.is_seller}
    if profile.is_buyer:
        return render(request, "buyer_home.html", context=context)
    if profile.is_seller:
        return render(request, "seller_home.html", context=context)


def get_models(request):
    manufacturer = request.GET.get('manufacturer')
    models = Car.objects.filter(manufacturer=manufacturer).values_list('model', flat=True)
    return JsonResponse(list(models), safe=False)


def get_years(request):
    manufacturer = request.GET.get('manufacturer')
    model = request.GET.get('model')
    years = Car.objects.filter(manufacturer=manufacturer, model=model).values_list('year', flat=True)
    return JsonResponse(list(years), safe=False)


def car_search(request):
    if not request.user.is_authenticated:
        return redirect("/login/")
    if request.method == "POST":
        selected_manufacturer = request.POST.get('manufacturer')
        selected_model = request.POST.get('model')
        selected_year = request.POST.get('year')
        car = Car.objects.filter(manufacturer=selected_manufacturer, model=selected_model, year=selected_year).get()
        return redirect('part_search_with_car', car_id=car.pk)

    profile = Profile.objects.get(user=request.user)
    context = {"is_buyer": profile.is_buyer, "is_seller": profile.is_seller}
    manufacturers = Car.objects.values_list('manufacturer', flat=True).distinct()
    context["manufacturers"] = manufacturers
    return render(request, "search_by_car.html", context=context)


def part_search(request, car_id=None):
    if not request.user.is_authenticated:
        return redirect("/login/")
    profile = Profile.objects.get(user=request.user)
    context = {"is_buyer": profile.is_buyer, "is_seller": profile.is_seller}
    if car_id:
        car = get_object_or_404(Car, pk=car_id)
        context["car"] = car

    return render(request, "search_by_part.html", context=context)


def item_list(request, category, car_id=None):
    if not request.user.is_authenticated:
        return redirect("/login/")
    profile = Profile.objects.get(user=request.user)
    context = {"is_buyer": profile.is_buyer, "is_seller": profile.is_seller}
    if car_id:
        car = get_object_or_404(Car, pk=car_id)
        parts = Product.objects.filter(cars=car, category=category)
        context["parts"] = parts
    else:
        parts = Product.objects.filter(category=category)
        context["parts"] = parts
    context["category"] = category
    return render(request, "item_list.html", context=context)


def add(request):
    if not request.user.is_authenticated:
        return redirect("/login/")
    profile = Profile.objects.get(user=request.user)
    context = {"is_buyer": profile.is_buyer, "is_seller": profile.is_seller, "form": AddProductForm()}
    if profile.is_seller:
        if request.method == "POST":
            form_data = AddProductForm(data=request.POST, files=request.FILES)
            if form_data.is_valid():
                product = form_data.save(commit=False)
                product.seller = request.user
                product.image = form_data.cleaned_data["image"]
                product.save()
                return redirect("seller_parts")
    else:
        return redirect("/login/")
    return render(request, "add.html", context=context)


def seller_parts(request):
    if not request.user.is_authenticated:
        return redirect("/login/")
    profile = Profile.objects.get(user=request.user)
    context = {"is_buyer": profile.is_buyer, "is_seller": profile.is_seller,
               "parts": Product.objects.filter(seller=request.user).all()}
    return render(request, "seller_parts.html", context=context)


def part_details(request, id):
    if not request.user.is_authenticated:
        return redirect("/login/")
    profile = Profile.objects.get(user=request.user)
    context = {"is_buyer": profile.is_buyer, "is_seller": profile.is_seller}
    part = get_object_or_404(Product, pk=id)
    context["part"] = part
    is_in_cart = False
    if profile.is_buyer:
        cart = ShoppingCart.objects.get(user=request.user)
        is_in_cart = cart.cart_items.filter(product=part).exists()
    context["is_in_cart"] = is_in_cart

    return render(request, "part_details.html", context=context)


def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect("/login/")
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, pk=product_id)

        cart, created = ShoppingCart.objects.get_or_create(user=request.user)
        cart_item, created = cart.cart_items.get_or_create(product=product)
        cart_item.quantity = quantity
        cart_item.save()

    return redirect(request.META.get('HTTP_REFERER', 'home'))


def remove_from_cart(request, product_id):
    pass


def shopping_cart(request):
    if not request.user.is_authenticated:
        return redirect("/login/")
    profile = Profile.objects.get(user=request.user)
    context = {"is_buyer": profile.is_buyer, "is_seller": profile.is_seller}

    cart = ShoppingCart.objects.get(user=request.user)
    cart_items = cart.cart_items.select_related('product')
    context["cart_items"] = cart_items

    total = cart_items.annotate(
        item_total=F('product__price') * F('quantity')
    ).aggregate(cart_total=Sum('item_total'))['cart_total'] or 0

    context["total"] = total

    return render(request, "shopping_cart.html", context=context)
