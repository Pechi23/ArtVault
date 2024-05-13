from .models import Gallery
from django.forms import ModelForm

class GalleryForm(ModelForm):
    class Meta:
        model = Gallery
        fields = ['title', 'description', 'cover']