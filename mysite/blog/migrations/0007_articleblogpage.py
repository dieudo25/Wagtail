# Generated by Django 3.1.2 on 2020-10-23 11:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0022_uploadedimage'),
        ('blog', '0006_auto_20201023_1108'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleBlogPage',
            fields=[
                ('blogdetailpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='blog.blogdetailpage')),
                ('subtitle', models.CharField(blank=True, max_length=100, null='')),
                ('intro_image', models.ForeignKey(blank=True, help_text='Best size for this image will be 1200x400', null=True, on_delete=django.db.models.deletion.SET_NULL, to='wagtailimages.image')),
            ],
            options={
                'abstract': False,
            },
            bases=('blog.blogdetailpage',),
        ),
    ]
