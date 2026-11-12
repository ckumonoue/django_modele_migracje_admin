from decimal import Decimal

from django import forms

CATEGORIES = [
    ("laptops", "Laptopy"),
    ("accessories", "Akcesoria"),
    ("monitors", "Monitory"),
]


class ProductForm(forms.Form):
    name = forms.CharField(
        label="Nazwa",
        max_length=100,
        min_length=3,
        widget=forms.TextInput(attrs={"class": "wide"}),
    )
    price = forms.DecimalField(label="Cena", min_value=Decimal("0.01"), max_digits=8, decimal_places=2)
    category = forms.ChoiceField(label="Kategoria", choices=CATEGORIES)
    is_available = forms.BooleanField(label="Dostępny", required=False, initial=True)
    description = forms.CharField(label="Opis", widget=forms.Textarea, required=False)

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if name.lower() in {"test", "asdf"}:
            raise forms.ValidationError("Wpisz prawdziwą nazwę produktu.")
        return name

    def clean(self):
        cleaned = super().clean()
        price = cleaned.get("price")
        category = cleaned.get("category")
        if price is not None and category == "laptops" and price < 500:
            self.add_error("price", "Laptop za mniej niż 500 zł? Sprawdź cenę.")
        return cleaned


class SearchForm(forms.Form):
    q = forms.CharField(label="Szukaj", required=False, max_length=50)
    only_available = forms.BooleanField(label="Tylko dostępne", required=False)
