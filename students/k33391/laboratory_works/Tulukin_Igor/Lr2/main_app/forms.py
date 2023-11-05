from django import forms
from .models import User, Ticket, Comment


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "password", "first_name", "last_name", "email", "passport"]


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["seat"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["rating", "message"]
