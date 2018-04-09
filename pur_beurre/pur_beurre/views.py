from django.shortcuts import render


def home(request):
    context = {'title': 'Mon super titre'}
    return render(request, 'food/home.html', context)

def account(request):
    form = AccountForm(request.POST or None)
    if form.is_valid():
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        send = True
    return render(request, 'food/account.html', local())

def credits(request):
    context = {'title': 'Mon super titre'}
    return render(request, 'food/credits.html', context)