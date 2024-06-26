# Generated by Django 5.0.2 on 2024-02-24 12:30

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sitepages', '0003_remove_product_color_product_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='I am an Amazing Vendor', null=True),
        ),
    ]
