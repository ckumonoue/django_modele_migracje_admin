from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import ProductForm, SearchForm
from .models import Product

ITEMS = [
    {"id": 1, "name": "Laptop", "price": 2999, "category": "laptops", "is_available": True},
    {"id": 2, "name": "Mysz", "price": 49, "category": "accessories", "is_available": False},
    {"id": 3, "name": "Klawiatura", "price": 199, "category": "accessories", "is_available": True},
    {"id": 4, "name": "Monitor", "price": 899, "category": "monitors", "is_available": True},
    {"id": 5, "name": "Słuchawki", "price": 149, "category": "accessories", "is_available": False},
]


def index(request):
    return render(request, "shop/index.html", {"project_name": "Sklep 4TP", "user_name": "ckumonoue"})


def about(request):
    return HttpResponse("Jesteśmy klasą 4TP. Robimy sklep internetowy.")


def contact(request):
    return HttpResponse("Kontakt: sklep@example.com, tel. 123 456 789")


def terms(request):
    return HttpResponse("Regulamin sklepu: zamówienia realizujemy w 2 dni robocze.")


def info(request):
    return JsonResponse({"name": "django_start", "author": "ckumonoue", "version": "0.1"})


def forbidden(request):
    return HttpResponse("Brak dostępu", status=403)


def hello(request, name):
    return HttpResponse(f"Cześć, {name}!")


def hello_age(request, name, age):
    return HttpResponse(f"Cześć, {name}! Masz {age} lat.")


def add(request, a, b):
    return HttpResponse(f"{a} + {b} = {a + b}")


def subtract(request, a, b):
    return HttpResponse(f"{a} - {b} = {a - b}")


def multiply(request, a, b):
    return HttpResponse(f"{a} * {b} = {a * b}")


def divide(request, a, b):
    if b == 0:
        return HttpResponse("Nie dzielimy przez zero", status=400)
    return HttpResponse(f"{a} / {b} = {a / b}")


def product_slug(request, slug):
    return HttpResponse(f"Produkt: {slug}")


def item_list(request):
    return render(request, "shop/item_list.html", {"items": ITEMS})


def item_detail(request, item_id):
    item = next((i for i in ITEMS if i["id"] == item_id), None)
    if item is None:
        raise Http404("Nie ma takiego przedmiotu")
    return render(request, "shop/item_detail.html", {"item": item})


def start(request):
    return redirect("shop:index")


def links(request):
    lines = [
        reverse("shop:about"),
        reverse("shop:hello", args=["Ania"]),
        reverse("shop:item_detail", args=[3]),
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain; charset=utf-8")


def product_list(request):
    form = SearchForm(request.GET)
    products = Product.objects.select_related("category")
    if form.is_valid():
        q = form.cleaned_data["q"]
        if q:
            products = products.filter(name__icontains=q)
        if form.cleaned_data["only_available"]:
            products = products.filter(is_available=True)
    return render(request, "shop/product_list.html", {"products": products, "form": form})


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, "shop/product_detail.html", {"product": product})


def product_add(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("shop:product_list")
    else:
        form = ProductForm()
    return render(request, "shop/product_form.html", {"form": form, "title": "Nowy produkt"})
