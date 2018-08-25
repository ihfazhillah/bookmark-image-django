import requests
from django import forms
from django.utils.text import slugify
from django.core.files.base import ContentFile
from .models import Image


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'url', 'description']
        widgets = {
            'url': forms.HiddenInput
        }

    def clean_url(self):
        valid_exts = ['jpeg', 'jpg', 'png']
        url = self.cleaned_data['url']
        ext = url.split('.')[-1].lower()

        if ext not in valid_exts:
            raise forms.ValidationError('Not a valid image, please change another url')
        return url

    def save(self, commit=True, force_insert=False, force_update=False):
        image_instance = super(ImageCreateForm, self).save(commit=False)
        image_url = self.cleaned_data['url']
        image_name = '{}.{}'.format(slugify(image_instance.title),
                                    image_url.split('.')[-1].lower())

        image_content = requests.get(image_url).content
        image_instance.image.save(image_name,
                                  ContentFile(image_content),
                                  save=False)

        if commit:
            image_instance.save()
        return image_instance





