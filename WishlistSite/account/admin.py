from django.contrib import admin

from .models import CustomUser, Gift, Wishlist

admin.site.register(CustomUser)
admin.site.register(Gift)
admin.site.register(Wishlist)