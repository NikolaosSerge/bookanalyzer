from django.forms import ModelForm
from .models import Book

class BookForm(ModelForm):
    """docstring for BookForm."""
    class Meta:
        model = Book
        fields = ['title','contents']
