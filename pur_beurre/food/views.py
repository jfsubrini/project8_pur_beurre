"""All the views for the food app of the pur_beurre project."""


# Django imports
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User #####
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# from django.core.exceptions import ObjectDoesNotExist  #####
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.detail import DetailView  #### Si on garde la vue générique FoodInfo


# Imports from my app
from .models import NutritionGrade, Category, Food, MySelection
from .forms import AccountForm, ValidationErrorList, ConnexionForm



####### CREATION DE COMPTE #######
def register(request):
    """View to the user account creation page and validation of the user form."""
    # Analysis and treatment of the register form that has been sent.
    if request.method == "POST":
        form = AccountForm(request.POST, error_class=ValidationErrorList)
        if form.is_valid():
            # form.save() ###
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username, email, password) ###
            user = authenticate(request, username=username, email=email, password=password)
            # If data are valid, automatic log in and redirection to 'Mon Compte' page.
            login(request, user)
            return redirect('account')
    else:
        form = AccountForm()

    # What to render
    context = {
        'form': form,
        'errors': form.errors.items()
        }
    return render(request, 'food/register.html', context)


####### MON COMPTE #######
@login_required(login_url='/account/register/', redirect_field_name='redirection_vers')
def account(request):
    """View to the user account information page."""
    return render(request, 'food/account.html')


####### CONNEXION #######
def signin(request):
    """View to the log in page."""
    signin_failed = False

    # In case the user is already logged in, redirection to homepage.
    if request.user.is_authenticated:
        return redirect('home')

    # Analysis and treatment of the sign in form that has been sent.
    if request.method == "POST":
        form = ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            # If the connexion is valid, log in and redirection to 'Mon Compte' page.
            if user is not None:
                login(request, user)
                return redirect('account')
            else:
                signin_failed = True
    else:
        form = ConnexionForm()

    # What to render
    context = {
        'form': form,
        'signin_failed': signin_failed
        }
    return render(request, 'food/signin.html', context)


####### DECONNEXION #######
def signout(request):
    """Log out function with redirection to homepage."""
    logout(request)
    return redirect('home')


####### RESULTATS DE LA RECHERCHE #######
def foodresult(request):
    """View to the page that displays all the substitute food products
    related to the category searched by the user."""

    query = request.GET.get('query')
    if not query:
        return render(request, 'food/home.html')
        # raise Http404 ### A importer

    # Parsing of the query to better find the query product
    #  into the database, searching by name AND brand.
    query = query.split(',')
    query_name = query[0].strip()
    query_brand = query[1].strip()
    # If the user entered a product name AND a product brand (after the comma).
    if query_brand:
        try:
            food_search = Food.objects.filter(
                name__icontains=query_name,
                brand__icontains=query_brand)
            food_search = food_search.order_by('name', 'brand')[0].get()
        except Food.DoesNotExist:
            return None
    # If the user only entered a product name.
    else:
        try:
            food_search = Food.objects.filter(
                name__icontains=query_name)
            food_search = food_search.order_by('name')[0].get()
        except Food.DoesNotExist:
            return None

    # Query expressions to find into the db the substitutes products :
    # same category and better nutrition_grade than the food_search.
    substitutes = Food.objects.filter(
        category=food_search.category,
        nutrition_grade__lt=food_search.nutrition_grade)
    substitutes = substitutes.distinct('name', 'brand')

    # OR
    # substitutes_cat = Category.objects.get(name=food_search.category)
    # substitutes = substitutes.cat.food.category.filter(nutrition_grade__lt=food_search.nutrition_grade)
    # substitutes = substitutes.distinct('name', 'brand')

    # Pagination : no more than 6 substitute products in a page.
    paginator = Paginator(substitutes, 6)
    page = request.GET.get('page')
    try:
        substitutes = paginator.page(page)
    except PageNotAnInteger:
        substitutes = paginator.page(1)
    except EmptyPage:
        substitutes = paginator.page(paginator.num_pages)

    # What to render
    context = {
        'food_search': food_search,
        'substitutes': substitutes,
        'paginate': True
    }
    return render(request, 'food/foodresult.html', context)


# ####### PAGE D'INFORMATION SUR L'ALIMENT #######
# def foodinfo(request, pk):
#     """View to the page that gives food information for each product."""
#     food_info = get_object_or_404(Food, pk=pk)

#     # What to render
#     context = {
#         'food_info': food_info
#     }
#     return render(request, 'food/foodinfo.html', context)


####### PAGE D'INFORMATION SUR L'ALIMENT #######
class FoodInfo(DetailView):
    """ Generic View for the foodinfo page : 'Page Aliment' """
    context_object_name = "food_info"
    model = Food
    template_name = "food/foodinfo.html"


####### PAGE DE SELECTION DES ALIMENTS SAINS PAR L'UTILISATEUR #######
@login_required(login_url='/account/signin/', redirect_field_name='redirection_vers')
def selection(request):
    """View to the user's personal selection of healthy food."""

    selected_deleted = False

    # If the user wants to delete a selected healthy food from is portofolio
    if request.method == 'POST':
        food_saved_delete = request.POST.get('food_saved_delete')
        food_saved_delete = MySelection.objects.get(pk=food_saved_delete.id)
        if food_saved_delete:
            food_saved_delete.delete()
            selected_deleted = True

    # Getting the list of all the selected healthy foods by the user
    foods_saved = MySelection.objects.filter(user=request.user)

    # What to render
    context = {
        'foods_saved': foods_saved,
        'selected_deleted': selected_deleted
    }

    return render(request, 'food/selection.html', context)
