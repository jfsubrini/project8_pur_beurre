#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module that use the OpenFoodFacts API to collect all the data needed for the pur_beurre database.

"""


from pprint import pprint
import requests



class OpenFoodFacts_API:
    """ Class that collect all the data needed for 10 categories from the OpenFoodFacts API."""

    """ Class instance : 10 different categories of food."""
    CATEGORIES_LIST = ['Chips et frites', 'Confitures', \
                        'Crêpes et galettes', 'Desserts au chocolat', \
                        'Gâteaux', 'Pâtes à tartiner', 'Petit-déjeuners', \
                        'Salades composées', 'Sandwichs', 'Tartes']


    def __init__(self, query):
        """Initializer / Instance Attributes"""
        self.user_query = query


    def categories(self):
        """Method that take each category from the class instance list and requests
        the data needed for pur_beurre database from the OFF API."""
        i = 0
        while i < 10:
            for category in OpenFoodFacts_API.CATEGORIES_LIST:
                self.user_query = category
                def getFoodData(user_query):
                    """Request to the Open Food Facts REST API to collect data for one category."""
                    URL = "https://fr.openfoodfacts.org/cgi/search.pl?"
                    payload = {'search_terms': self.user_query, 'page_size': 1000, 'json': 1}
                    response = requests.get(URL, params=payload)
                    openfoodfacts = response.json()
                    j = 0
                    # for item in range(0, len(openfoodfacts['products'])):
                    for item in range(0, openfoodfacts['count']):
                        try:
                            self.nutrition_grade = openfoodfacts['products'][item]['nutrition_grade_fr']
                            if self.nutrition_grade:
                                self.name = openfoodfacts['products'][item]['product_name']
                                self.image_food = openfoodfacts['products'][item]['image_front_url']
                                self.image_nutrition = openfoodfacts['products'][item]['image_nutrition_url']
                                self.nutrition_grade = openfoodfacts['products'][item]['nutrition_grade_fr']
                                self.nutrition_score = openfoodfacts['products'][item]['nutriments']['nutrition-score-fr_100g']
                                self.url = openfoodfacts['products'][item]['url']
                                # pprint(openfoodfacts)
                                j += 1
                                pprint(self.name)
                                pprint(self.image_food)
                                pprint(self.image_nutrition)
                                pprint(self.nutrition_grade)
                                pprint(self.nutrition_score)
                                pprint(self.url)
                                print(category)
                                print(j, '\n')
                                # return self.name, self.image_food, self.image_nutrition, \
                                # self.nutrition_grade, self.nutrition_score, self.url, category
                        except:
                            pass
                getFoodData(self.user_query)
                i += 1


query = OpenFoodFacts_API('blabla')

query.categories()

########################################################
# print("La base de données pur_beurre a bien été mise à jour")
