"""All the views for the food app of the pur_beurre project."""


# Django imports
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect  ## get_ if foodinfo not generic
from django.views.generic.detail import DetailView  ## Si on garde la vue générique FoodInfo
from django.http import Http404


# Imports from my app
from .models import NutritionGrade, Category, Food, MySelection  ## Nutri & Cat unused ?
from .forms import AccountForm, ValidationErrorList  ## Viré ConnexionForm



####### CREATION DE COMPTE #######
def register(request):
    """View to the user account creation page and validation of the user form."""
    # Analysis and treatment of the register form that has been sent.
    if request.method == "POST":
        form = AccountForm(request.POST, error_class=ValidationErrorList)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username, email, password)
            user = authenticate(request, username=username, email=email, password=password)
            # If data are valid, automatic log in and redirection to 'Mon Compte' page.
            login(request, user)
            return redirect('account')
    else:
        form = AccountForm()

    # What to render to the template.
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


####### RESULTATS DE LA RECHERCHE #######
def foodresult(request):
    """View to the page that displays all the substitute food products
    related to the category searched by the user. Possibility to save an healthy product."""

    query = request.GET.get('query')
    if not query:
        return render(request, 'food/home.html')

    ##########            PARSING            ##########
    # Parsing of the query to better find the query product
    # into the database, searching by name AND brand, if informed by the user.
    query = query.split(',')
    try:
        query_name = query[0].strip().lower().capitalize()
        query_brand = query[1].strip().lower().capitalize()
    except IndexError:
        query_name = query[0].strip().lower().capitalize()
        query_brand = None

    ##########    DISPLAY SUBSTITUTE FOODS   ##########
    # If the user entered a product name AND a product brand (after the comma).
    if query_name and query_brand:
        try:
            food_search = Food.objects.filter(
                name__icontains=query_name,
                brand__icontains=query_brand)[:1].get()
        except Food.DoesNotExist:
            raise Http404("Votre requête ne permet pas de récupérer un aliment dans notre base de données.\nEssayez une autre requête.")
    # If the user only entered a product name.
    elif query_name:
        try:
            food_search = Food.objects.filter(
                name__icontains=query_name)[:1].get()
        except Food.DoesNotExist:
            raise Http404("Votre requête ne permet pas de récupérer un aliment dans notre base de données.\nEssayez une autre requête.")
    # Query expression to find into the database the substitutes products
    # with the same category and better nutrition_grade than the food_search.
    substitutes = {}
    try:
        substitutes = Food.objects.filter(
            category=food_search.category,
            nutrition_grade__lt=food_search.nutrition_grade)
        substitutes = substitutes.distinct('name', 'brand')
    # substitutes = substitutes.order_by('nutrition_grade', 'nutrition_score') ## TROUVER DE QUOI TRIER
    except:
        return substitutes

    ##########      SAVE AN HEALTHY FOOD     ##########
    # If the user wants to save an healthy food for is portfolio.
    food_selected = False
    if request.user.is_authenticated and request.method == 'POST':
        food_saved = request.POST.get('food_id')
        food_saved = Food.objects.filter(id=food_saved)
        # Verify if this food has been already selected by the user.
        verify = MySelection.objects.filter(my_healthy_foods=food_saved, user=request.user)
        # The case that the food has been already selected by the user.
        if verify.exists():
            food_selected = False
        # The case it's a new selected food by the user.
        else:
            MySelection.objects.create(my_healthy_foods=food_saved[0], user=request.user)
            food_selected = True

    # Pagination : no more than 6 substitute products in a page.
    paginator = Paginator(substitutes, 6)
    page = request.GET.get('page')
    try:
        substitutes = paginator.page(page)
    except PageNotAnInteger:
        substitutes = paginator.page(1)
    except EmptyPage:
        substitutes = paginator.page(paginator.num_pages)

    # What to render to the template.
    context = {
        'food_search': food_search,
        'substitutes': substitutes,
        'food_selected': food_selected,
        'paginate': True,
    }
    return render(request, 'food/foodresult.html', context)


# ####### PAGE D'INFORMATION SUR L'ALIMENT #######
# def foodinfo(request, pk):
#     """View to the page that gives food information for each product."""
#     food_info = get_object_or_404(Food, pk=pk)

#   # What to render to the template.
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
    """View to the user's personal selection of healthy food.
    Possibility to delete a selected product."""

    # Getting the list of all the selected healthy foods by the user.
    foods_saved = MySelection.objects.filter(user=request.user)

    # If the user wants to delete a selected healthy food from is portfolio.
    selected_deleted = False
    if request.method == 'POST':
        food_saved_delete = request.POST.get('food_saved_delete')
        food_saved_delete = MySelection.objects.get(pk=food_saved_delete.id)
        if food_saved_delete:
            food_saved_delete.delete()
            selected_deleted = True

    # Pagination : no more than 6 substitute products in a page.
    paginator = Paginator(substitutes, 6)
    page = request.GET.get('page')
    try:
        substitutes = paginator.page(page)
    except PageNotAnInteger:
        substitutes = paginator.page(1)
    except EmptyPage:
        substitutes = paginator.page(paginator.num_pages)

    # What to render to the template.
    context = {
        'foods_saved': foods_saved,
        'selected_deleted': selected_deleted,
        'paginate': True
    }
    return render(request, 'food/selection.html', context)
