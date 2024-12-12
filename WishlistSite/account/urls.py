from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('<str:username>', views.WishlistsView.as_view(), name='wishlists'),
    path('wishlist/<str:slug>', views.GiftsView.as_view(), name='wishlist'),
    path('reserved/<str:wishlist_slug>/<str:slug>', views.reserved_gift, name='reserved'),
    path('check-username-email/', views.check_username_email, name='check-username-email'),
]