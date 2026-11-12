# django_modele_migracje_admin

Materiał 12 – Django: modele, migracje, admin. Projekt `config`, aplikacja `shop` (kontynuacja materiału 11).

## Uruchomienie

```powershell
python --version                 # wymagane 3.12+
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Serwer: http://127.0.0.1:8000, panel admina: http://127.0.0.1:8000/admin/

## Struktura (MTV)

| Warstwa | Plik | Co tam jest |
|---|---|---|
| **Model** | `shop/models.py` | `Category`, `Product`, `gross_price()`, relacja `ForeignKey` |
| **Template** | `shop/templates/shop/*.html` | wyświetlanie (`base.html`, listy, szczegóły, formularz) |
| **View** | `shop/views.py` | `objects.filter`, `get_object_or_404`, `form.save()`, `redirect` |
| formularz | `shop/forms.py` | `ModelForm` + własna walidacja, `SearchForm` |
| routing | `config/urls.py`, `shop/urls.py` | mapa adresów |
| migracje | `shop/migrations/` | historia schematu bazy (idzie do Gita) |
| admin | `shop/admin.py` | zaplecze dla zespołu |

`db.sqlite3` jest w `.gitignore` (to dane, nie kod), a `migrations/` **nie** (to historia bazy – bez niej po `git clone` nie da się odtworzyć tabel).

## Trasy

| Metoda | Adres | Nazwa trasy | Opis |
|---|---|---|---|
| GET | `/` | `shop:index` | strona główna |
| GET | `/products/?q=&only_available=` | `shop:product_list` | lista produktów z bazy, wyszukiwarka |
| GET, POST | `/products/add/` | `shop:product_add` | dodawanie (ModelForm) |
| GET | `/products/<id>/` | `shop:product_detail` | szczegóły, 404 gdy brak |
| GET, POST | `/products/<id>/edit/` | `shop:product_edit` | edycja (`instance`) |
| POST | `/products/<id>/delete/` | `shop:product_delete` | usuwanie, GET → 405 |
| GET | `/products/<slug>/` | `shop:product_slug` | produkt po slugu (z materiału 10) |
| GET | `/items/`, `/items/<id>/` | `shop:item_list`, `shop:item_detail` | lista `ITEMS` z materiału 11 |
| GET | `/about/`, `/contact/`, `/terms/`, `/api/info/`, `/admin-panel/` | `shop:about` … | strony z materiału 10 |
| GET | `/hello/…`, `/add/…`, `/subtract/…`, `/multiply/…`, `/divide/…` | `shop:hello` … | trasy dynamiczne z materiału 10 |
| GET | `/start/`, `/links/` | `shop:start`, `shop:links` | redirect i `reverse` |
| GET | `/admin/` | – | panel admina Django |

## Notatki

### Zadanie 2 – migracje

`python manage.py makemigrations` tworzy `shop/migrations/0001_initial.py` (operacja `CreateModel` z listą pól), a `python manage.py migrate` wykonuje go na bazie `db.sqlite3`.

`python manage.py sqlmigrate shop 0001` pokazuje SQL (oczekiwany wynik – **wklej własny z terminala**):

```sql
BEGIN;
--
-- Create model Product
--
CREATE TABLE "shop_product" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL, "price" decimal NOT NULL, "is_available" bool NOT NULL, "description" text NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL);
COMMIT;
```

### Zadanie 3 – zmiana modelu

Dodane pole `stock = PositiveIntegerField("stan magazynowy", default=0)` → drugi plik `0002_product_stock.py` (`AddField`). Po `migrate` dane z zadania 4 zostają w tabeli, bo zmiana schematu jest migracją, a nie usuwaniem bazy.

`python manage.py showmigrations shop` (oczekiwany wynik – **wklej własny**):

```text
shop
 [X] 0001_initial
 [X] 0002_product_stock
```

### Zadanie 4 – CRUD w konsoli (`python manage.py shell`)

Przebieg sesji (oczekiwany – **zastąp własnym wydrukiem z konsoli**):

```python
>>> from decimal import Decimal
>>> from shop.models import Product
>>> p = Product(name="Laptop", price=Decimal("2999.00"))
>>> p.save()                                            # save()
>>> Product.objects.create(name="Mysz", price=49, is_available=False)   # create()
<Product: Mysz>
>>> Product.objects.create(name="Klawiatura", price=199)
<Product: Klawiatura>
>>> Product.objects.all()
<QuerySet [<Product: Klawiatura>, <Product: Laptop>, <Product: Mysz>]>   # ordering = ["name"]
>>> Product.objects.get(name="Mysz")
<Product: Mysz>
>>> Product.objects.filter(price__gte=100, name__icontains="lap")      # dwa lookupy
<QuerySet [<Product: Laptop>]>
>>> Product.objects.order_by("-price")
<QuerySet [<Product: Laptop>, <Product: Klawiatura>, <Product: Mysz>]>
>>> Product.objects.filter(is_available=False).update(price=0)         # hurtowo
1
>>> print(Product.objects.filter(is_available=True).query)
SELECT "shop_product"."id", "shop_product"."name", ... FROM "shop_product" WHERE "shop_product"."is_available" ORDER BY "shop_product"."name" ASC
>>> Product.objects.get(name="Mysz").delete()
(1, {'shop.Product': 1})
```

### Zadanie 5 – relacja `Product` → `Category`

`Category` (`name`, `slug`) i `ForeignKey(Category, on_delete=PROTECT, related_name="products")` w `Product`. Migracja `0003` tworzy kategorię, dodaje do niej istniejące produkty (kategoria „Inne”) i dopiero wtedy dodaje kolumnę `category_id` – dzięki temu `migrate` nie wymaga kasowania bazy, mimo że pole nie jest `null`.

Sesja w konsoli (oczekiwana – **zastąp własnym wydrukiem**):

```python
>>> from shop.models import Category, Product
>>> lap = Category.objects.create(name="Laptopy", slug="laptops")
>>> acc = Category.objects.create(name="Akcesoria", slug="accessories")
>>> Product.objects.create(name="Laptop Dell", price=2999, category=lap)
>>> Product.objects.create(name="Mysz Logitech", price=49, category=acc)
>>> p = Product.objects.get(name="Mysz Logitech")
>>> p.category                              # produkt -> kategoria
<Category: Akcesoria>
>>> acc.products.all()                      # kategoria -> produkty (related_name)
<QuerySet [<Product: Mysz Logitech>]>
>>> Product.objects.filter(category__slug="laptops")   # lookup przez relację
<QuerySet [<Product: Laptop Dell>]>
>>> lap.delete()
ProtectedError: Cannot delete some instances of model 'Category' because they are referenced through protected foreign keys: 'Product.category'.
```

### Zadanie 6 – panel admina

Superużytkownik: `python manage.py createsuperuser`. Oba modele są zarejestrowane w `shop/admin.py` z `list_display`, `list_filter`, `search_fields` i `list_editable` (cena i dostępność edytowane bezpośrednio na liście). Panel: `/admin/`.

### Zadanie 7 – widoki na modelach

Lista słowników `PRODUCTS` została usunięta. `product_list` korzysta z `Product.objects.select_related("category")` (jeden `JOIN` zamiast zapytania o kategorię dla każdego produktu – problem N+1), wyszukiwarka z materiału 11 używa `filter(name__icontains=q)` i `filter(is_available=True)`. `product_detail` używa `get_object_or_404`. Szablony korzystają z `p.pk`, `p.category` i `p.gross_price`.

Strony `/items/` z materiałów 10 i 11 nadal działają na liście słowników `ITEMS` (nie są częścią tego zadania).

### Zadanie 8 – ModelForm

`ProductForm` dziedziczy po `forms.ModelForm`, a pola bierze z modelu `Product` (`fields` wypisane jawnie, bez `"__all__"`). Pole `category` jest automatycznie `<select>` z kategoriami z bazy. `widgets` zachowuje klasę CSS `wide` z materiału 11, a własna walidacja zostaje (`clean_name`, `clean()`); `clean_price` i minimalna długość nazwy są w formularzu, bo model nie ma tych ograniczeń. Widok dodawania zapisuje przez `form.save()`.

Liczba linii (niepustych):

| | `forms.Form` (zad. 7) | `ModelForm` (zad. 8) |
|---|---|---|
| definicje pól (`Meta` w nowej wersji) | 10 | 4 |
| cała klasa `ProductForm` | 23 | 24 |

Definicje pól skróciły się z 10 do 4 linii. Cała klasa wyszła o jedną linię dłuższa, bo doszły `clean_price` i sprawdzenie długości nazwy, które wcześniej dawały pola formularza.

### Zadanie 9 – edycja i usuwanie

`product_edit` używa tego samego formularza i szablonu co dodawanie; `ProductForm(request.POST, instance=product)` nadpisuje istniejący produkt, a `title` w kontekście zmienia nagłówek. `product_delete` ma `@require_POST` i jest wywoływany formularzem POST (z `{% csrf_token %}`) z listy produktów.

Sprawdzenie (**potwierdź u siebie**):

- GET na `/products/<id>/delete/` → **405 Method Not Allowed**; widok w ogóle się nie uruchamia.
- Edycja bez `instance` (`ProductForm(request.POST)`) → zapis tworzy **nowy** produkt zamiast zmienić stary, więc na liście pojawia się duplikat.
