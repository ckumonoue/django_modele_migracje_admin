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

Zrzut ekranu tabeli `shop_product` z DB Browser for SQLite: **DODAJ do `docs/`**.

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

Superużytkownik: `python manage.py createsuperuser`. Oba modele są zarejestrowane w `shop/admin.py` z `list_display`, `list_filter`, `search_fields` i `list_editable` (cena i dostępność edytowane bezpośrednio na liście). Panel: `/admin/`. Zrzut ekranu listy produktów (5 rekordów wpisanych przez admina): **DODAJ do `docs/`**.
