import django.db.models.deletion
from django.db import migrations, models


def create_default_category(apps, schema_editor):
    """Istniejące produkty (sprzed tej migracji) trafiają do kategorii "Inne"."""
    Category = apps.get_model("shop", "Category")
    Category.objects.get_or_create(pk=1, defaults={"name": "Inne", "slug": "inne"})


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0002_product_stock"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50, unique=True, verbose_name="nazwa")),
                ("slug", models.SlugField(unique=True)),
            ],
            options={
                "verbose_name": "kategoria",
                "verbose_name_plural": "kategorie",
                "ordering": ["name"],
            },
        ),
        migrations.RunPython(create_default_category, migrations.RunPython.noop),
        migrations.AddField(
            model_name="product",
            name="category",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="products",
                to="shop.category",
                verbose_name="kategoria",
            ),
            preserve_default=False,
        ),
    ]
