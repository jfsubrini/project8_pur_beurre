"""All the tests for the food app of the pur_beurre project."""


# Django imports
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


# Imports from my app
from .models import NutritionGrade, Category, Food, MySelection



################################################################
#                      ACCUEIL PUR BEURRE                      #
################################################################

class HomepageTestCase(TestCase):
    """Testing that the homepage will be returned with a HTTP 200
    and the home template.
    """

    def test_homepage(self):
        """Testing that all home named views returns HTTP 200 and the right template.
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'food/home.html')

    def test_homepage2(self):
        """Testing that typing '/' returns HTTP 200 and the right template.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'food/home.html')

    def test_homepage3(self):
        """Testing that typing '/index/' returns HTTP 200 and the right template.
        """
        response = self.client.get('/index/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'food/home.html')

    def test_homepage4(self):
        """Testing that typing '/home/' returns HTTP 200 and the right template.
        """
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'food/home.html')


################################################################
#                       MENTIONS LEGALES                       #
################################################################

class ImprintTestCase(TestCase):
    """Testing that typing '/imprint'
    returns HTTP 200 and the imprint template.
    """

    def test_imprint_page(self):
        """Testing that typing '/imprint/' returns HTTP 200 and the right template.
        """
        response = self.client.get(reverse('imprint'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'food/imprint.html')


################################################################
#                          MON COMPTE                          #
################################################################

class MyAccountTestCase(TestCase):
    """Testing the User Account page.
    """

    def setUp(self):
        """Data samples to run the tests.
        """
        self.username = 'jeanfrancois'
        self.email = 'jfsubrini@yahoo.com'
        self.password = 'monsupermotdepasse'
        self.user = User.objects.create_user(self.username, self.email, self.password)

    def test_account_logged_in(self):
        """Accessing the user account page while logged in
        that renders HTTP 200 and the right template.
        """
        # The user is logged in.
        self.client.login(username=self.username, password=self.password)
        # Testing the access while logged in.
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'food/account.html')

    def test_account_logged_out(self):
        """Trying to access the user account page while logged out that renders
        HTTP 302, redirection to the user register page.
        """
        response = self.client.get(reverse('account'))
        self.assertRedirects(
            response, (reverse('register'))+'?redirection_vers='+(reverse('account')))


################################################################
#                      CREATION DE COMPTE                      #
################################################################

class RegisterTestCase(TestCase):
    """
    Testing the User Register page.
    """

    def setUp(self):
        """Data samples to run the tests.
        """
        self.username = 'jeanfrancois'
        self.email = 'jfsubrini@yahoo.com'
        self.password = 'monsupermotdepasse'
        # self.user = User.objects.create_user(self.username, self.email, self.password)

    def test_register_page(self):
        """Connexion to the Register page that must return HTTP 200 and the right template.
        """
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'food/register.html')

    def test_register_valid(self):
        """Post a valid form from the Register page that must return
        the account page (HTTP 302 url redirection).
        The user must be registered into the database.
        """
        response = self.client.post(reverse('register'), {
            'username': self.username,
            'email': self.email,
            'password': self.password
        })
        self.assertRedirects(response, '/account/')
        self.assertEqual(
            User.objects.filter(
                username=self.username, email=self.email).exists(),
            True
        )

    def test_register_invalid(self):
        """Post an invalid form from the Sign In page that must return
        HTTP 200 and stay in the same page with the right template.
        The user mustn't be registred into the database.
        """
        response = self.client.post(reverse('register'), {
            'username': 'blabla',
            'email': 'blablaagain',
            'password': 'moreblabla'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'food/register.html')
        self.assertEqual(
            User.objects.filter(
                username=self.username, email=self.email, password=self.password).exists(),
            False
        )


################################################################
#                          CONNEXION                           #
################################################################

class SignInTestCase(TestCase):
    """
    Testing the Sign In page.
    """

    def setUp(self):
        """Data samples to run the tests.
        """
        self.username = 'jeanfrancois'
        self.email = 'jfsubrini@yahoo.com'
        self.password = 'monsupermotdepasse'
        self.user = User.objects.create_user(self.username, self.email, self.password)

    def test_signin_page(self):
        """Connexion to the Sign In page that must return HTTP 200 and the right template.
        """
        response = self.client.get(reverse('signin'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'food/signin.html')

    def test_signin_valid(self):
        """Post a valid form from the Sign In page that must return
        the account page (HTTP 302 url redirection).
        """
        response = self.client.post(reverse('signin'), {
            'username': self.username,
            'password': self.password
        })
        self.assertRedirects(response, '/account/')

    def test_signin_invalid(self):
        """Post an invalid form from the Sign In page that must return
        HTTP 200 and stay in the same page with the right template.
        """
        response = self.client.post(reverse('signin'), {
            'username': 'blabla',
            'password': 'moreblabla'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'food/signin.html')


################################################################
#                           RESULTATS                          #
################################################################

class FoodResultTestCase(TestCase):
    """
    Testing the Food Result page.
    """

# def setUp(self):
#         """Data samples to run the tests.
#         """
#         self.username = 'jeanfrancois'
#         self.email = 'jfsubrini@yahoo.com'
#         self.password = 'monsupermotdepasse'
#         self.user = User.objects.create_user(self.username, self.email, self.password)

#         # Sample of food data.
#         food = {
#             'id_food': '3017620429484',
#             'name': 'Nutella',
#             'brand': 'Ferrero',
#             'category': 6,
#             'nutrition_grade': 'E',
#             'nutrition_score': 26,
#             'url': 'https://fr.openfoodfacts.org/produit/3017620429484/nutella-ferrero',
#             'image_food': '???',
#             'image_nutrition': '???',
#             'category': Category.objects.create(name="Pâte à tartiner")
#         }
#         nutella = Food.objects.create(**food)
#         food.save()
#         self.food = food

#         # Sample of substitute food data.
#         substitute = {
#             'id_dish': '???',
#             'name': "Pâte à tartiner",
#             'url': "???",
#             'grade': "???",
#             'pic': "???",
#             "category": self.dish.category
#         }
#         substitute = Food.objects.create(**substitute)
#         substitute.save()
#         self.substitute = substitute

##### Connexion avec et sans log in  #######

    def test_foodresult_valid(self):
        """Accessing the foodresult page while the user query is valid.
        This must return HTTP 200 and the right template.
        """
        response = self.client.get(reverse('foodresult'), {'query': 'Nutella'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'food/foodresult.html')

    def test_foodresult_invalid_404(self):
        """Accessing the foodresult page while the user query is invalid.
        This must return HTTP 404 and the right template.
        """
        response = self.client.get(reverse('foodresult'), {'query': '????????????'})
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_foodresult_save(self):
        """Saving a substitute food into MySelection table
        while the user is logged in.
        ############ renvoie page aliment ##############
        """

        # The user is logged in.
        self.client.login(username=self.username, password=self.password)

        # # Testing the saving of a substitute food.
        # path = reverse('foodresult')+'/?query=Nutella'
        # response = self.client.post(path, {"substitute": self.substitute.id})
        # self.assertEqual(response.status_code, 200)

        # The substitute food must be registered into MySelection table.
        self.assertEqual(
            MySelection.objects.all().exists(),
            True
        )

    def test_foodresult_not_saved(self):
        """Not saving a substitute food into MySelection table
        while the user is logged in, because of invalid data.
        """

        # The user is logged in.
        self.client.login(username=self.username, password=self.password)

        ######

        # The substitute food mustn't be registered into MySelection table.
        self.assertEqual(
            MySelection.objects.filter(id=1).exists(),
            False
        )


################################################################
#                         MES ALIMENTS                         #
################################################################

class SelectionTestCase(TestCase):
    """
    Testing the Selection page.
    """

    def setUp(self):
        """Data samples to run the tests.
        """
        self.username = 'jeanfrancois'
        self.email = 'jfsubrini@yahoo.com'
        self.password = 'monsupermotdepasse'
        self.user = User.objects.create_user(self.username, self.email, self.password)

        # Sample of category and food data.
        category = Category.objects.create(name="Pâtes à tartiner")

        # food = {
        #     'food_id': '3333',
        #     'name': 'Nutella',
        #     'brand': 'Ferrero',
        #     'category': 6,
        #     'nutrition_grade': 'E',
        #     'nutrition_score': 26,
        #     'url': 'https://fr.openfoodfacts.org/produit/3017620429484/nutella-ferrero',
        #     'image_food': 'https://static.openfoodfacts.org/images/products/301/762/042/9484/front_fr.147.400.jpg',
        #     'image_nutrition': 'https://static.openfoodfacts.org/images/products/301/762/042/9484/nutrition_fr.106.400.jpg',
        # }
        food = {
            'food_id': '3333',
            'name': "Purée crue noisette",
            'brand': "Perl'Amande",
            'category': Category.objects.get(name=category),  ### NON
            'nutrition_grade': 'C',
            'nutrition_score': 7,
            'url': 'https://fr.openfoodfacts.org/produit/3267110001038/puree-crue-noisette-perl-amande',
            'image_food': 'https://static.openfoodfacts.org/images/products/326/711/000/1038/front_fr.17.400.jpg',
            'image_nutrition': 'https://static.openfoodfacts.org/images/products/326/711/000/1038/nutrition_fr.18.400.jpg',
        }
        puree_noisette = Food.objects.create(**food)
        
        # puree_noisette as a selected food by the user.
        self.food = MySelection.objects.create(puree_noisette)

    def test_selection_logged_in(self):
        """Connexion to the Selection page that must return HTTP 200,
        if logged in, with the right food selection and the right template.
        """
        # The user is logged in.
        self.client.login(username=self.username, password=self.password)
        # Testing the access while logged in.
        response = self.client.get(
            reverse('selection', args=(self.food.id,))
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'food/selection.html')

    def test_selection_logged_out(self):
        """Trying to access the Selection page while logged out that renders
        HTTP 302, redirection to the Sign In page.
        """
        response = self.client.get(
            reverse('selection', args=(self.food.id,))
            )
        self.assertRedirects(
            response, (reverse('signin'))+'?redirection_vers='+(reverse('selection')))

    def test_selection_empty(self):
        """Connexion to the Selection page that must return HTTP 200,
        with an empty food selection.
        """
        response = self.client.get(
            reverse('selection', args=None)
            )
        self.assertEqual(response.status_code, 200)


################################################################
#                         PAGE ALIMENT                         #
################################################################

class FoodInfoTestCase(TestCase):
    """
    Testing the Food Info page.
    """

    def setUp(self):
        """Data sample to run the tests.
        """
        nutella = Food.objects.create(name='Nutella')
        self.food = Food.objects.get(name='Nutella')

    def test_foodinfo_200(self):
        """Connexion to the FoodInfo page that must return HTTP 200
        if the pk exists (food id). Returns the right template.
        """
        pk = self.pk
        response = self.client.get(reverse('foodinfo', args=(pk)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'food/foodinfo.html')

    def test_foodinfo_404(self):
        """Connexion to the FoodInfo page that must return HTTP 404
        if the pk doesn't exist (food id). Returns the 404 page.
        """
        pk = 0
        response = self.client.get(reverse('foodinfo', args=(pk)))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

##### connexion sans log in et avec à food info ? #######

################################################################
#                          DECONNEXION                         #
################################################################

class SignOutTestCase(TestCase):
    """
    Testing the Sign Out process.
    """

    def setUp(self):
        """Data samples to run the tests.
        """
        self.username = 'jeanfrancois'
        self.email = 'jfsubrini@yahoo.com'
        self.password = 'monsupermotdepasse'
        self.user = User.objects.create_user(self.username, self.email, self.password)

    def test_signout(self):
        """The user is already logged in and wants to log out.
        """
        # The user is logged in.
        self.client.login(username=self.username, password=self.password)
        # Testing the log out with the return HTTP 200 and the display of the homepage template.
        response = self.client.get(reverse('signout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'food/home.html')


################################################################
#  OPEN FOOD FACTS API - POPULATION OF THE PUR_BEURRE DATABASE #
################################################################

class OFFAPITestCase(TestCase):
    """
    Testing ....
    """

    def bbbb(self):
        """Testing ....
        """
        pass
