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
