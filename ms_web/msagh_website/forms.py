from django import forms
from .models import Spot


class SpotForm(forms.ModelForm):
    class Meta:
        model = Spot
        fields = ['title',
                  'content',
                  ]

        labels = {
            'title': 'Tytuł',
            'content': 'Treść'
        }

        widgets = {
            'title' : forms.TextInput(attrs={'class':'form-group'}),
            'content': forms.Textarea(attrs={'class': 'form-group'})

        }