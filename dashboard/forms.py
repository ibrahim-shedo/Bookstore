# dashboard/forms.py
from django import forms
from store.models import Book, Category, Writer

from django.core.exceptions import ValidationError


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'  # Include all fields from the Book model except 'created' and 'updated'

    # Define ModelChoiceFields for Category and Writer
    writer = forms.ModelChoiceField(
        queryset=Writer.objects.all(),
        empty_label="Select a writer",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Select a category",
        widget=forms.Select(attrs={'class': 'form-control'})
    )



class WriterForm(forms.ModelForm):
    class Meta:
        model = Writer
        fields = ['name', 'slug', 'bio', 'pic']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'icon']

    name = forms.CharField(
        label='Category Name',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category Name...'})
    )
    slug = forms.SlugField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Slug'
    )
    icon = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'custom-file-input'}),
        label='Icon'
    )
