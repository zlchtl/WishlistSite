from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from .models import CustomUser, Wishlist, Gift
from django.views import View
from . import forms

class RegisterView(View):
    """Логика ответа на запрос о регистрации"""

    def get(self, request): #реагирование на get запрос
        form = forms.RegistrationForm()
        return render(request, 'account/register.html', {'form': form})
    def post(self, request):  #реагирование на post запрос
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            newuser = form.save()
            login(request, newuser)
            return redirect('index')
        return render(request, 'account/register.html', {'form': form})

class LoginView(View):
    """Логика ответа на запрос об авторизации"""

    def get(self, request):
        form = forms.LoginForm()
        return render(request, 'account/login.html', {'form': form})
    def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            username = form.cleaned_data['username']
            login(request, authenticate(username=username, password=password))
            return redirect('index')
        return render(request, 'account/login.html', {'form': form})

class WishlistsView(View):
    """Логика ответа на запрос о просмотре вишлистов конкретного пользователя"""

    def get(self, request, username):
        if CustomUser.username_exists(username):
            user = CustomUser.objects.filter(username=username).first()
            wishlists = Wishlist.objects.filter(user=user).all()
            show_form = (request.user == user)
            form = forms.WishlistForm()
            return render(request, 'account/wishlists.html', {'form': form, 'wishlists': wishlists, 'show_form':show_form, 'username':user})
        return redirect('register')
    def post(self, request, username):
        if CustomUser.username_exists(username):
            user = CustomUser.objects.filter(username=username).first()
            wishlists = Wishlist.objects.filter(user=user).all()
            show_form = (request.user == user)
        else:
            return redirect('register')
        if not CustomUser.username_exists(request.user) :
            return redirect('register')
        form = forms.WishlistForm(request.POST)
        if form.is_valid():
            form.save(user = request.user)
        wishlists = Wishlist.objects.filter(user=request.user).all()
        return render(request, 'account/wishlists.html', {'form': form, 'wishlists': wishlists, 'show_form':show_form, 'username':user})

class GiftsView(View):
    """Логика ответа на запрос о просмотре подарков конкретного вишлиста"""

    def get(self, request, slug):
        wishlist = get_object_or_404(Wishlist, slug=slug)
        gifts = wishlist.products.all()
        show_form = (request.user == wishlist.user)
        context = {
            'wishlist': wishlist,
            'gifts': gifts,
            'show_form': show_form,
            'form': forms.GiftForm() if show_form else None,
        }
        return render(request, 'account/wishlist.html', context)

    def post(self, request, slug):
        wishlist = get_object_or_404(Wishlist, slug=slug)
        if request.user != wishlist.user:
            return redirect('wishlist', slug = slug)
        form = forms.GiftForm(request.POST)

        if form.is_valid():
            new_gift = form.save()
            wishlist.products.add(new_gift)
            return redirect('wishlist', slug = slug)

        context = {
            'wishlist': wishlist,
            'gifts': wishlist.products.all(),
            'form': form,
        }
        return render(request, 'account/wishlist.html', context)

def reserved_gift(request, wishlist_slug, slug):
    """Логика резервирования подарка по его слагу и перенаправление на страницу вишлиста для обновления списка"""

    if request.method == 'GET':
        gift = get_object_or_404(Gift, slug=slug)
        gift.reserved = not(gift.reserved)
        gift.save()
        return redirect('wishlist', slug = wishlist_slug)

def logout_view(request):
    """Логика выхода из аккаунта и перенаправление на домашнюю страницу"""

    logout(request)
    return redirect('index')

def check_username_email(request):
    """
    Логика ответа на запрос о проверке свободного email или username в БД.
    Ожидается запрос от JS со страницы регистрации.
    """

    if request.method == 'GET':
        username = request.GET.get('username')
        email = request.GET.get('email')
        data = {"result": False}
        if username is not None:
            data["result"] = CustomUser.username_exists(username)
        if email is not None:
            data["result"] = CustomUser.email_exists(email)
        return JsonResponse(data, status=200)
    else:
        return JsonResponse({"error": "Only GET method"}, status=400)