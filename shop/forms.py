from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "category", "is_available", "description"]
        widgets = {"name": forms.TextInput(attrs={"class": "wide"})}

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if len(name) < 3:
            raise forms.ValidationError("Nazwa musi mieć co najmniej 3 znaki.")
        if name.lower() in {"test", "asdf"}:
            raise forms.ValidationError("Wpisz prawdziwą nazwę produktu.")
        return name

    def clean_price(self):
        price = self.cleaned_data["price"]
        if price <= 0:
            raise forms.ValidationError("Cena musi być większa od zera.")
        return price

    def clean(self):
        cleaned = super().clean()
        price = cleaned.get("price")
        category = cleaned.get("category")
        if price is not None and category is not None and category.slug == "laptops" and price < 500:
            self.add_error("price", "Laptop za mniej niż 500 zł? Sprawdź cenę.")
        return cleaned


class SearchForm(forms.Form):
    q = forms.CharField(label="Szukaj", required=False, max_length=50)
    only_available = forms.BooleanField(label="Tylko dostępne", required=False)
