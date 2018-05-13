#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module that uses the OpenFoodFacts API to collect
all the data needed for the pur_beurre database.
"""


# Standard libraries imports
import requests

# Imports from my app
from constants import OFF_API_URL, CATEGORIES_LIST
from .models import Food, Category



class OpenFoodFactsAPI:
    """ Class that collects all the data needed for all selected categories
    from the OpenFoodFacts API.
    """

    def __init__(self, query=''):
        """Initializer / Instance Attributes"""
        self.query = query
        self.name = ""
        self.brand = ""
        self.image_food = ""
        self.image_nutrition = ""
        self.nutrition_grade = ""
        self.nutrition_score = ""
        self.url = ""

    def categories(self):
        """Method that maintains equivalence between the categories present in the
        CATEGORIES_LIST and the ones prensent into the database Category table."""
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
        i = 0
        while i < len(CATEGORIES_LIST):
            for category in CATEGORIES_LIST:
                self.query = category
                print("Collecte des informations sur les aliments de la catégorie : \
                    '{}' ...".format(self.query))

                def get_cat_data(self):
                    """Request to the OFF API to collect data for one category."""
                    payload = {'search_terms': self.query, 'page_size': 1000, 'json': 1}
                    response = requests.get(OFF_API_URL, params=payload)
                    openfoodfacts = response.json()
                    j = 0
                    for item in range(0, openfoodfacts['count']-1):
                        try:
                            # If the product item has these data then collects them all.
                            shortcut = openfoodfacts['products'][item]
                            self.name = shortcut['product_name']
                            self.brand = shortcut['brands']
                            self.image_food = shortcut['image_front_url']
                            self.image_nutrition = shortcut['image_nutrition_url']
                            self.nutrition_grade = shortcut['nutrition_grade_fr']
                            self.nutrition_score = shortcut['nutriments']['nutrition-score-fr_100g']
                            self.url = shortcut['url']
                            j += 1
                            print("Nom : {}".format(self.name))
                            print("Marque : {}".format(self.brand))
                            print("Image de l'aliment : {}".format(self.image_food))
                            print("Image repères nutritionnels : {}".format(self.image_nutrition))
                            print("Nutriscore : {}".format(self.nutrition_grade))
                            print("Autre nutriscore : {}".format(self.nutrition_score))
                            print("URL fiche aliment : {}".format(self.url))
                            print("Catégorie : {}".format(self.query))
                            print("N° de l'aliment : {}\n".format(j))
                            InsertAllData.insert(self.name, self.brand, self.query, \
                                self.image_food, self.image_nutrition, self.nutrition_grade, \
                                self.nutrition_score, self.url)
                        except:
                            pass
                get_cat_data(self.query)
                i += 1


class InsertAllData(OpenFoodFactsAPI):
    """ Class that inserts all the data into pur_beurre database.
    """

    def insert(self):
        """Inserting each data from each category into the Food table."""
        Food.objects.create(
            name=self.name,
            brand=self.brand,
            category=Category.objects.get(name=self.query),
            nutrition_grade=self.nutrition_grade,
            nutrition_score=self.nutrition_score,
            url=self.url,
            image_food=self.image_food,
            image_nutrition=self.image_nutrition)


instance = OpenFoodFactsAPI()
instance.categories()
instance.get_all_data()

print("La base de données pur_beurre a bien été mise à jour.\nBon appétit !")
