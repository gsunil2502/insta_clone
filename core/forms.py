from django import forms
from django.forms import fields, models, widgets
from core.models import Post
class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text','image')
        widgets = {
            'text' : forms.Textarea(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Caption this......',
                'id': 'captionarea'

            })
        }