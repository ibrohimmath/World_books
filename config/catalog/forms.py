from django import forms 

from datetime import date 

from catalog.models import Book

class AuthorsForm(forms.Form):
    first_name = forms.CharField(label = 'Muallifning ismi')
    last_name = forms.CharField(label = 'Muallifning familiyasi')
    date_of_birth = forms.DateField(
        label = 'Tug\'ilgan sanasi',
        initial = format(date.today()),
        widget = forms.widgets.DateInput(attrs = {'type': 'date'})
    )
    date_of_death = forms.DateField(
        label = 'O\'lim sanasi',
        initial = format(date.today()),
        widget = forms.widgets.DateInput(attrs = {'type': 'date'})
    )
    
class BookModelForm(forms.ModelForm):
    class Meta:
        model = Book 
        fields = ['title', 'genre', 'language', 'author', 'summary', 'isbn']
        
