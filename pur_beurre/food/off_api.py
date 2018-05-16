#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module that uses the OpenFoodFacts API to collect
all the data needed for the pur_beurre database.
"""


# Standard libraries imports
import requests

# Django imports
from django.db import transaction, IntegrityError

# Imports from my app
from constants import OFF_API_URL, CATEGORIES_LIST
from models import Food, Category



class OpenFoodFactsAPI:
    """ Class that collects all the data needed for all selected categories
    from the OpenFoodFacts API.
    """

    @transaction.atomic
    def categories(self):
        """Method that maintains equivalence between the categories present in the
        CATEGORIES_LIST and the ones present into the database Category table."""
        db_actual_cat = Category.objects.values_list('name', flat=True)
        for list_cat in CATEGORIES_LIST:
            if list_cat not in db_actual_cat:
                # Creation of a new category into the database.
                Category.objects.create(name=list_cat)
        for db_cat in db_actual_cat:
            if db_cat not in CATEGORIES_LIST:
                # Delete of the category presents into the database
                # but not anymore into the CATEGORIES_LIST.
                Category.objects.filter(name=db_cat).delete()

    def get_all_data(self):
        """Request for each food category all the data needed, collecting from
        the Open Food Facts REST API."""
        for category in CATEGORIES_LIST:
            print("Collecte des informations sur les aliments de la catégorie : \
                '{}' ...".format(category))
            """Request to the OFF API to collect data for one category."""
            payload = {'search_terms': category, 'page_size': 1000, 'json': 1}
            response = requests.get(OFF_API_URL, params=payload)
            openfoodfacts = response.json()
            j = 0
            for item in range(0, openfoodfacts['count']-1):                
                # If the product item has these data then collects them all.
                try:
                    shortcut = openfoodfacts['products'][item]
                    name = shortcut['product_name']
                    brand = shortcut['brands']
                    image_food = shortcut['image_front_url']
                    image_nutrition = shortcut['image_nutrition_url']
                    nutrition_grade = shortcut['nutrition_grade_fr']
                    nutrition_score = shortcut['nutriments']['nutrition-score-fr_100g']
                    url = shortcut['url']
                    j += 1
                    # Call to the function that inserts the food values into the database.
                    InsertAllData.insert(name, brand, category, nutrition_grade, \
                        nutrition_score, url, image_food, image_nutrition, j)
                except:
                    pass


class InsertAllData(OpenFoodFactsAPI):
    """ Class that inserts all the data into pur_beurre database.
    """

    def insert(name, brand, category, nutrition_grade, nutrition_score, \
        url, image_food, image_nutrition, j):
        """Inserting into the Food table all the data for each new food of one category."""
        try:
            with transaction.atomic():
                Food.objects.create(
                    name=name,
                    brand=brand,
                    category=Category.objects.get(name=category),
                    nutrition_grade=nutrition_grade,
                    nutrition_score=nutrition_score,
                    url=url,
                    image_food=image_food,
                    image_nutrition=image_nutrition)
                # Prints for the console
                print("Nom : {}".format(name))
                print("Marque : {}".format(brand))
                print("Image de l'aliment : {}".format(image_food))
                print("Image repères nutritionnels : {}".format(image_nutrition))
                print("Nutriscore : {}".format(nutrition_grade))
                print("Autre nutriscore : {}".format(nutrition_score))
                print("URL fiche aliment : {}".format(url))
                print("Catégorie : {}".format(category))
                print("N° de l'aliment : {}\n".format(j))
        except IntegrityError:
                print("Problème : {} n'a pas pu être enregistré dans la base de données.".format(name))



instance = OpenFoodFactsAPI()
instance.categories()
instance.get_all_data()

print("La base de données pur_beurre a bien été mise à jour.\nBon appétit !")
