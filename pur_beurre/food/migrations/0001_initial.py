# Generated by Django 2.0.3 on 2018-04-29 07:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import enumchoicefield.fields
import food.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='catégorie')),
            ],
            options={
                'verbose_name': 'catégorie',
            },
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name="nom de l'aliment")),
                ('brand', models.CharField(default='rien', max_length=100, verbose_name="marque de l'aliment")),
                ('nutrition_grade', enumchoicefield.fields.EnumChoiceField(enum_class=food.models.NutritionGrade, max_length=1, verbose_name='nutriscore')),
                ('nutrition_score', models.SmallIntegerField(verbose_name='autre nutriscore')),
                ('url', models.URLField(verbose_name="url de la fiche de l'aliment")),
                ('image_food', models.URLField(verbose_name="url de l'image de l'aliment")),
                ('image_nutrition', models.URLField(verbose_name="url de l'image des repères nutritionnels de l'aliment")),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='food.Category', verbose_name='catégorie')),
            ],
            options={
                'verbose_name': 'aliment',
            },
        ),
        migrations.CreateModel(
            name='MySelection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('my_healthy_foods', models.ManyToManyField(related_name='healthy_foods_selection', to='food.Food', verbose_name='mes aliments sains')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'ma sélection',
            },
        ),
        migrations.AlterUniqueTogether(
            name='food',
            unique_together={('name', 'brand')},
        ),
    ]
