from django.db import models
# from enumchoicefield import ChoiceEnum, EnumChoiceField



# class NutritionGrade(ChoiceEnum):
#     a = "A"
#     b = "B"
#     c = "C"
#     d = "D"
#     e = "E"


# class MyAccount(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField(max_length=100)
#     password = models.CharField(max_length=100)


#     class Meta:
#         verbose_name = "utilisateur"


#     def __str__(self):
#         return self.name


# class Category(models.Model):
#     name = models.CharField(max_length=100)


#     class Meta:
#         verbose_name = "catégorie"


#     def __str__(self):
#         return self.name


# class Food(models.Model):
#     name = models.CharField(max_length=255, unique=True)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     nutrition_grade = EnumChoiceField(NutritionGrade)
#     nutrition_score = models.SmallIntegerField()
#     url = models.URLField()
#     image_food = models.URLField(null=True)  ## null ?
#     image_score = models.URLField(null=True)  ## null ?
#     image_nutrition = models.URLField(null=True)  ## null ?


#     class Meta:
#         verbose_name = "aliment"


#     def __str__(self):
#         return self.name


# class MyHealthyFood(models.Model):
#     food = models.OneToOneField(Food)
#     # myaccount = models.ManyToManyField(MyAccount, blank=True) ### A REVOIR blank, ligne de code ici ?


#     class Meta:
#         verbose_name = "sélection"


#     def __str__(self):
#         return self.food
