from django.urls import path

from . import views

app_name = "shop"

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("terms/", views.terms, name="terms"),
    path("api/info/", views.info, name="info"),
    path("admin-panel/", views.forbidden, name="forbidden"),
    path("hello/<str:name>/", views.hello, name="hello"),
    path("hello/<str:name>/<int:age>/", views.hello_age, name="hello_age"),
    path("add/<int:a>/<int:b>/", views.add, name="add"),
    path("subtract/<int:a>/<int:b>/", views.subtract, name="subtract"),
    path("multiply/<int:a>/<int:b>/", views.multiply, name="multiply"),
    path("divide/<int:a>/<int:b>/", views.divide, name="divide"),
    path("products/", views.product_list, name="product_list"),
    path("products/add/", views.product_add, name="product_add"),
    path("products/<int:product_id>/", views.product_detail, name="product_detail"),
    path("products/<slug:slug>/", views.product_slug, name="product_slug"),
    path("items/", views.item_list, name="item_list"),
    path("items/<int:item_id>/", views.item_detail, name="item_detail"),
    path("start/", views.start, name="start"),
    path("links/", views.links, name="links"),
]
