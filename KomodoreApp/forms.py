from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from KomodoreApp.models import Product


class RegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"
            field.field.widget.attrs["style"] = "border-radius: 20px; border: 2px solid #2165F6;"
            field.field.widget.attrs["placeholder"] = field.label
            field.label = ""
            field.help_text = ''

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control w-75 mx-auto',
            'style': 'border-radius: 20px; border: 2px solid #2165F6;',
            'placeholder': 'Username',
        }),
        label='',
        help_text='',
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control w-75 mx-auto',
            'style': 'border-radius: 20px; border: 2px solid #2165F6;',
            'placeholder': 'Password',
        }),
        label='',
        help_text='',
    )


class AddProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddProductForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"
            field.field.widget.attrs["style"] = "border-radius: 20px; border: 2px solid #2165F6;"
            field.field.widget.attrs["placeholder"] = field.label
            field.label = ""
            field.help_text = ""

        self.fields["image"].widget.attrs["accept"] = "image/*"
        self.fields["characteristics"].widget.attrs["rows"] = 6
        self.fields["description"].widget.attrs["rows"] = 4
        self.fields["characteristics"].widget.attrs["cols"] = 40
        self.fields["description"].widget.attrs["cols"] = 40
        self.fields["category"].widget.attrs["class"] = "form-select"
        self.fields["warranty"].widget.attrs["class"] = "form-select"

    class Meta:
        model = Product
        exclude = ("seller", )
