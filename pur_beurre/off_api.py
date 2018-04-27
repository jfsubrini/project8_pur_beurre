#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module that use the OpenFoodFacts API to collect all the data needed for the pur_beurre database.

"""


from pprint import pprint
import requests

from food.models import Food, Category



class OpenFoodFacts_API:
    """ Class that collect all the data needed for 10 categories from the OpenFoodFacts API."""

    # Class instance : 10 different categories of food.
    CATEGORIES_LIST = ['Chips et frites', 'Confitures', \
                        'Crêpes et galettes', \
                        'Desserts au chocolat', \
                        'Gâteaux', 'Pâtes à tartiner', \
                        'Petit-déjeuners', 'Salades composées', \
                        'Sandwichs', 'Tartes']


    def __init__(self, query=''):
        """Initializer / Instance Attributes"""
        self.user_query = query


    def categories(self):
        """Method that take each category from the class instance list and requests
        the data needed for pur_beurre database from the OFF API."""
        i = 0
        while i < len(OpenFoodFacts_API.CATEGORIES_LIST):
            for category in OpenFoodFacts_API.CATEGORIES_LIST:
                self.user_query = category
                
                def getFoodData(user_query):
                    """Request to the Open Food Facts REST API to collect data for one category."""
                    URL = "https://fr.openfoodfacts.org/cgi/search.pl?"
                    payload = {'search_terms': self.user_query, 'page_size': 1000, 'json': 1}
                    response = requests.get(URL, params=payload)
                    openfoodfacts = response.json()
                    j = 0
                    for item in range(0, openfoodfacts['count']):
                        try:
                            self.nutrition_grade = openfoodfacts['products'][item]['nutrition_grade_fr']
                            if self.nutrition_grade:
                                self.name = openfoodfacts['products'][item]['product_name']
                                self.brand = openfoodfacts['products'][item]['brands']
                                self.image_food = openfoodfacts['products'][item]['image_front_url']
                                self.image_nutrition = openfoodfacts['products'][item]['image_nutrition_url']
                                self.nutrition_grade = openfoodfacts['products'][item]['nutrition_grade_fr']
                                self.nutrition_score = openfoodfacts['products'][item]['nutriments']['nutrition-score-fr_100g']
                                self.url = openfoodfacts['products'][item]['url']
                                j += 1
                                pprint(self.name)
                                pprint(self.brand)
                                pprint(self.image_food)
                                pprint(self.image_nutrition)
                                pprint(self.nutrition_grade)
                                pprint(self.nutrition_score)
                                pprint(self.url)
                                print(category, '\n')
                                # Insert each new category name in the Category table.
                                if j == 1:
                                    Category.objects.create(name=category)
                                # Insert each data in the Food table.
                                Food.objects.create(
                                    name=self.name,
                                    brand=self.brand,
                                    category=Category.objects.get(category_id), #######?????
                                    nutrition_grade=self.nutrition_grade,
                                    nutrition_score=self.nutrition_score,
                                    url=self.url,
                                    image_food=self.image_food,
                                    image_nutrition=self.image_nutrition)
                        except:
                            pass
                getFoodData(self.user_query)
                i += 1


query = OpenFoodFacts_API()

query.categories()


########################################################
# print("La base de données pur_beurre a bien été mise à jour")
