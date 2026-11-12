from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, verbose_name="nazwa")),
                ("price", models.DecimalField(decimal_places=2, max_digits=8, verbose_name="cena")),
                ("is_available", models.BooleanField(default=True, verbose_name="dostępny")),
                ("description", models.TextField(blank=True, verbose_name="opis")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "produkt",
                "verbose_name_plural": "produkty",
                "ordering": ["name"],
            },
        ),
    ]
