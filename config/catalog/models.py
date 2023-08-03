from django.db import models 
from django.contrib.auth import get_user_model

from django.urls import reverse

from datetime import date 

class Genre(models.Model):
    name = models.CharField(
        max_length = 200,
        help_text = 'Kitobning janrini kiriting',
        verbose_name = 'Kitobning janri',
    )
    
    def __str__(self):
        return self.name 
    
class Language(models.Model):
    name = models.CharField(
        max_length = 200,
        help_text = 'Kitobning tilini kiriting',
        verbose_name = 'Kitobning tili',
    )
    
    def __str__(self):
        return self.name 
    
class Author(models.Model):
    first_name = models.CharField(
        max_length = 100,
        help_text = 'Muallifning ismini kiriting',
        verbose_name = 'Muallifning ismi',
    )
    last_name = models.CharField(
        max_length = 100,
        help_text = 'Muallifning familiyasini kiriting',
        verbose_name = 'Muallifning familiyasi',
    )
    date_of_birth = models.DateField(
        help_text = 'Tug\'ilgan sanasini kiriting',
        verbose_name = 'Tug\'ilgan sanasi',
        null = True, blank = True,
    )    
    date_of_death = models.DateField(
        help_text = 'O\'lgan sanasini kiriting',
        verbose_name = 'O\'lim sanasi',
        null = True, blank = True,
    )

    def __str__(self):
        return self.last_name 
    
class Book(models.Model):
    title = models.CharField(
        max_length = 200,
        help_text = 'Kitobning nomini kiriting',
        verbose_name = 'Kitobning nomi',
    )
    genre = models.ForeignKey(
        'Genre', on_delete = models.CASCADE,
        help_text = 'Kitob uchun janr tanlang',
        verbose_name = 'Kitob janri', null = True,
    )
    language = models.ForeignKey(
        'Language', on_delete = models.CASCADE,
        help_text = 'Kitob uchun til tanlang',
        verbose_name = 'Kitob tili', null = True,
    )
    author = models.ManyToManyField(
        'Author',
        help_text = 'Kitobnign muallifini kiriting',
        verbose_name = 'Kitob muallifi',  
    )
    summary = models.CharField(
        max_length = 1000,
        help_text = 'Kitob uchun qisqa ta\'rif yozing',
        verbose_name = 'Kitob annotatsiyasi',
    )
    isbn = models.CharField(
        max_length = 13,
        help_text = '13 belgidan iborat bo\'lishi shart',
        verbose_name = 'Kitobning ISBN',
    )
    
    def __str__(self):
        return self.title 
    
    def get_absolute_url(self):
        return reverse('book-detail', args = [str(self.id)])
    
    def display_author(self):
        return ', '.join([author.last_name for author in self.author.all()])
    display_author.short_description = 'Mualliflar'
    
    
class Status(models.Model):
    name = models.CharField(
        max_length = 20,
        help_text = 'Kitobning nusxasini kiriting',
        verbose_name = 'Kitob nusxasining holati',
    )
    
    def __str__(self):
        return self.name 
    
class BookInstance(models.Model):
    book = models.ForeignKey('Book', on_delete = models.CASCADE, null = True)
    inv_nom = models.CharField(
        max_length = 20, null = True, 
        help_text = 'Kitob nusxasining inventariy nomerini kiriting',
        verbose_name = 'Inventariy nomer',
    )
    imprint = models.CharField(
        max_length = 200,
        help_text = 'Nashriyotni hamda ishlab chiqarilgan yilni kiriting',
        verbose_name = 'Nashriyot',
    )
    status = models.ForeignKey(
        'Status', on_delete = models.CASCADE,
        null = True, help_text = 'Kitob nusxasini holatini o\'zgartirish',
        verbose_name = 'Kitob nusxasining holati',
    )
    due_back = models.DateField(
        null = True, blank = True,
        help_text = 'Holatning muddatining sanasini kiriting',
        verbose_name = 'Holat tugashining muddat sanasi',
    )
    
    borrower = models.ForeignKey(
        get_user_model(), on_delete = models.SET_NULL,
        null = True, blank = True,
        verbose_name = 'Buyurtma beruvchi',
        help_text = 'Kitobga buyurtma beruvchini tanlang',        
    )
    
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True 
        return False
    
    def __str__(self):
        return '%s %s %s' %(self.inv_nom, self.book, self.status)