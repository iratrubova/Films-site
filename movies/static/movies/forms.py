from django import forms
from django.forms import fields

from .models import Reviews

class ReviewsForm(forms.ModelForm):

    class Meta:
        model = Reviews
        fields = ['name', 'email', 'text']