from django import forms
from .models import Spot,Meme,CommentSpot


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


class MemeForm(forms.ModelForm):
    class Meta:
        model = Meme
        fields = ['title',
                  'image'

                  ]

        labels = {
            'title': 'Tytuł',
            'image': 'Mem'

        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-group'}),


        }

class CommentSpotForm(forms.ModelForm):
    class Meta:
        model = CommentSpot
        fields = ['content']
        widgets = {

            'content': forms.Textarea(attrs={'class': 'form-group'},)

        }
