from django import forms
from .models import Image
from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'url', 'description', )
        widgets = {
            'url': forms.HiddenInput
        }

    def clean_url(self):
        """
        Sprawdza czy adres url kończy się na .jpg lub .jpeg.
        :return: adres url, jeśli poprawny
        """
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError('Podany adres URL nie zawiera obrazów w obsługiwanym formacie.')
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        image = super(ImageCreateForm, self).save(commit=False) # Zapisanie danych wpisanych w formularz
        image_url = self.cleaned_data['url']
        # Stworzenie nazwy obrazu, slugify title + rozszerzenie
        image_name = '{}.{}'.format(slugify(image.title), image_url.rsplit('.', 1)[1].lower())

        #Pobranie pliku
        response = request.urlopen(image_url)
        image.image.save(image_name, ContentFile(response.read()), save=False)
        if commit:
            image.save()
        return image