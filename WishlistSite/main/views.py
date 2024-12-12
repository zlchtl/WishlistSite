from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse, HttpResponseBadRequest
from account.models import CustomUser, Wishlist, Gift
import json

class IndexView(View):
    def get(self, request):
        CustomUser.username_exists(request.user)
        return render(request, 'main/index.html',{'user_is_authorized': CustomUser.username_exists(request.user), 'user': request.user})

    def post(self, request):
        username = request.POST.get('username')
        if username:
            try:
                user = CustomUser.objects.get(username=username)
                wishlists = Wishlist.objects.filter(user=user)
                if wishlists.exists():
                    return redirect('wishlists', username=user)
                else:
                    message = f"У пользователя '{username}' пока нет вишлистов."
            except CustomUser.DoesNotExist:
                message = f"Пользователь с именем '{username}' не найден."
        else:
            message = "Пожалуйста, укажите имя пользователя."

        context = {'message': message}
        return render(request, 'main/index.html', context)