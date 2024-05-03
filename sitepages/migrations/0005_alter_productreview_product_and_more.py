# Generated by Django 5.0.2 on 2024-02-24 19:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitepages', '0004_alter_product_description_alter_vendor_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productreview',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='review', to='sitepages.product'),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='rating',
            field=models.IntegerField(choices=[('1', '☆☆☆☆★'), ('2', '☆☆☆★★'), ('3', '☆☆★★★'), ('4', '☆★★★★'), ('5', '★★★★★')], default=None),
        ),
    ]