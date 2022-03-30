# Generated by Django 4.0.3 on 2022-03-17 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parse', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=100)),
                ('dictionary', models.TextField()),
                ('quantity', models.IntegerField(default=0)),
            ],
        ),
    ]