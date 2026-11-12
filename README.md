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
