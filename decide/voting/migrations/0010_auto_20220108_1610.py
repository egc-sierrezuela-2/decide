# Generated by Django 2.0 on 2022-01-08 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0009_auto_20220108_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='type',
            field=models.IntegerField(choices=[(4, 'EQUALITY'), (3, 'SAINTE_LAGUE'), (2, 'BORDA'), (1, 'DHONT'), (0, 'IDENTITY')], default=1),
        ),
    ]
