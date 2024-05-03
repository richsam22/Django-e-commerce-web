from django import forms
from .models import ProductReview, Profile

class ProductReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'write review '}))
    
    class Meta:
        model = ProductReview
        fields = ['review', 'rating']


class ProfileForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Full Name"}))
    bio = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Bio"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Phone"}))
    
    
    class Meta:
        model = Profile
        fields = ["full_name", "image", "bio", "phone"]