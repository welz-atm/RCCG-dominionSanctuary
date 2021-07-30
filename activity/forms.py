from django import forms
from .models import Comment, Service, Photo, Tithe, Donation


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ('date', 'name', 'announcement', 'video',)


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('image',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment_text',)


class TitheForm(forms.ModelForm):
    class Meta:
        model = Tithe
        fields = ('month', 'amount',)


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ('first_name', 'last_name', 'amount', 'telephone',)
