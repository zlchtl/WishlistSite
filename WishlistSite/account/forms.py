from django import forms
from .models import CustomUser, Wishlist, Gift
import re
from django.contrib.auth import authenticate

class RegistrationForm(forms.ModelForm):
    """Форма для регистрации нового пользователя"""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password again", widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'username']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = "Email"
        self.fields['username'].label = "Username"
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1 and len(password1)<8:
            raise forms.ValidationError("Password must be longer than 8 characters.")
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if username and not re.match(r'^[a-zA-Zа-яА-ЯёЁ0-9-_]+$', username):
            raise forms.ValidationError("The username must not contain special characters")
        if CustomUser.username_exists(username):
            raise forms.ValidationError("This username is already registered")
        return username


    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and not re.match(r'^[a-zA-Zа-яА-ЯёЁ0-9@.-_]+$', email):
            raise forms.ValidationError("The email must not contain special characters")
        if CustomUser.email_exists(email):
            raise forms.ValidationError("This email is already registered")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # Хэшируем пароль
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    """Упрощеная форма регистрации для авторизации нового пользователя"""

    username = forms.CharField(label="Username", max_length=150,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if username and not re.match(r'^[a-zA-Zа-яА-ЯёЁ0-9-_]+$', username):
            raise forms.ValidationError("The username must not contain special characters.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                self.add_error('password', "Invalid username or password.")
        return cleaned_data

class GiftForm(forms.ModelForm):
    """Форма для создания нового подарка"""

    class Meta:
        model = Gift
        fields = ['name', 'price', 'description', 'url']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = "Name"
        self.fields['price'].label = "Price"
        self.fields['description'].label = "Description"
        self.fields['url'].label = "Url"
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control small-textarea'

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if name and not re.match(r'^[a-zA-Zа-яА-ЯёЁ0-9 ]+$', name):
            raise forms.ValidationError("The name must not contain special characters")
        return name

    def save(self, commit=True):
        gift = super().save(commit=False) # Хэшируем пароль
        if commit:
            gift.save()
        return gift

class WishlistForm(forms.ModelForm):
    """Форма для создания нового вишлиста для подарков"""

    class Meta:
        model = Wishlist
        fields = ['event']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['event'].label = "Event name"
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def save(self, user, commit=True):
        wishlist = super().save(commit=False)
        wishlist.user = user
        if commit:
            wishlist.save()
        return wishlist
