# Generated by Django 3.1.2 on 2020-11-02 08:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('content', models.TextField()),
                ('image', models.ImageField(upload_to='')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Friends',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='person1', to=settings.AUTH_USER_MODEL)),
                ('person2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='person2', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
