# Generated by Django 3.1.2 on 2020-10-22 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subscribers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(help_text='Email address', max_length=100)),
                ('full_name', models.CharField(help_text='First and last name', max_length=100)),
            ],
        ),
    ]
