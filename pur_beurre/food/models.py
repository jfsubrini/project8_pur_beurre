"""All the models for the food app of the pur_beurre project."""


# Imports
from enumchoicefield import ChoiceEnum, EnumChoiceField

from django.db import models
from django.contrib.auth.models import User
# from django.conf import settings



class NutritionGrade(ChoiceEnum):
    """ENUM values for nutrition_grade."""
    a = "A"
    b = "B"
    c = "C"
    d = "D"
    e = "E"


class Category(models.Model):
    """To create the Category table in the database."""
    name = models.CharField("catégorie", max_length=100, unique=True)

    class Meta:
        verbose_name="catégorie"
    
    def __str__(self):
        return self.name


class Food(models.Model):
    """To create the Food table in the database with 8 attributs (fields)."""
    name = models.CharField("nom de l'aliment", max_length=255)
    brand = models.CharField("marque de l'aliment", max_length=100, null=False, default='rien')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='category', verbose_name="catégorie")
    nutrition_grade = EnumChoiceField(NutritionGrade, verbose_name="nutriscore")
    nutrition_score = models.SmallIntegerField("autre nutriscore")
    url = models.URLField("url de la fiche de l'aliment")
    image_food = models.URLField("url de l'image de l'aliment")
    image_nutrition = models.URLField("url de l'image des repères nutritionnels de l'aliment")

    class Meta:
        """Each (name + brand) item must be unique."""
        verbose_name="aliment"
        unique_together = ("name", "brand")

    def __str__(self):
        return self.name


class MySelection(models.Model):
    """To create the MySelection table in the database which stores
    the selected healthy foods of each user."""
    user = models.OneToOneField(User, on_delete=models.PROTECT, 
        related_name='user_selection', verbose_name="utilisateur")
    # user = models.OneToOneField(settings.AUTH_USER_MODEL)    
    my_healthy_foods = models.ManyToManyField(
        Food, related_name='healthy_foods_selection', verbose_name="mes aliments sains")
    # avec null=True ?

    class Meta:
        verbose_name="ma sélection"

    def __str__(self):
        return self.user

#### OR ... #####
# class MyAccount(models.Model):
#     username = models.CharField("nom d'utilisateur", max_length=100)
#     # username = models.OneToOneField(User, on_delete=models.PROTECT, related_name='user')
#     email = models.EmailField("email de l'utilisateur", max_length=100)
#     password = models.CharField("mot de passe de l'utilisateur", max_length=100)
#     my_healthy_foods = models.ManyToManyField(
#         Food, related_name='healthy_foods', verbose_name="mes aliments sains")

#     class Meta:
#         verbose_name="utilisateur"

#     def __str__(self):
#         return self.username      
