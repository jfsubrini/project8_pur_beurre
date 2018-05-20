# project8_pur_beurre

Program developed by Jean-François Subrini, May 2018.



## What the project is for ?

* **Pur Beurre** website allows you to find a substitute healthy food to your junk food !
* Food quality is based on the nutriscore, with all the data from the [Open Food Facts](https://fr.openfoodfacts.org) open source database.
* The user enters the name and the brand of the food to substitute. The website find a list of substitute foods from the same category and with a better [nutriscore](https://fr.openfoodfacts.org/score-nutritionnel-france).
* Cliking on each substitute food the user can have more information about it.
* If registered and signed in, the user can save the healthy products found in the substitute list and then consult his selection. Each selected food can also be deleted.


## How to use it or get it running ?

* Pur Beurre is a **Python website**, developed with the **Django** framework with a Creative Bootstrap Theme as the frontend.

* You can access the website from your Terminal executing *./manage.py runserver* and watching it from your *localhost:8000* in your favorite browser.

* You can also and more easily go directly online at [Pur Beurre](https://purbeurre8.herokuapp.com/) website, deployed with *Heroku*.


## How to update de category and food data ?

* Pur Beurre has been developped with 10 different categories of food. See the name of these categories in the **CATEGORIES_LIST** (*pur_beurre/food/constants.py*). If you want to change it - add some more or drop ones - just modify that list before running an update. 

* If you change the CATEGORIES_LIST or just want to update your database with the latest food data, you need to run this command from your command line : ***./manage.py off_api***.


***Enjoy it !***