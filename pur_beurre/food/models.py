"""All the models for the food app of the pur_beurre project"""


from django.db import models
from enumchoicefield import ChoiceEnum, EnumChoiceField



class NutritionGrade(ChoiceEnum):
    """ENUM values for nutrition_grade"""
    a = "A"
    b = "B"
    c = "C"
    d = "D"
    e = "E"


class MyAccount(models.Model):
    """To create the MyAccount table in the database"""
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)


    class Meta:
        verbose_name = "utilisateur"


    def __str__(self):
        return self.username


class Category(models.Model):
    """To create the Category table in the database"""
    name = models.CharField(max_length=100)


    class Meta:
        verbose_name = "catégorie"


    def __str__(self):
        return self.name


class Food(models.Model):
    """To create the Food table in the database"""
    name = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    nutrition_grade = EnumChoiceField(NutritionGrade)
    nutrition_score = models.SmallIntegerField()
    url = models.URLField()
    image_food = models.URLField(null=True)  ## null ?
    image_score = models.URLField(null=True)  ## null ?
    image_nutrition = models.URLField(null=True)  ## null ?


    class Meta:
        verbose_name = "aliment"


    def __str__(self):
        return self.name


class MyHealthyFood(models.Model):
    """To create the MyHealthyFood table in the database"""
    food = models.OneToOneField(Food, on_delete=models.CASCADE)
    # myaccount = models.ManyToManyField(MyAccount, blank=True) ### A REVOIR blank, code ici ?


    class Meta:
        verbose_name = "sélection"


    def __str__(self):
        return self.food
