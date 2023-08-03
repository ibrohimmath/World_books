from django.shortcuts import render, redirect, get_object_or_404 
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseNotFound, JsonResponse 
from django.urls import reverse_lazy

from django.views import generic 
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin

from catalog.models import Book, Author, BookInstance, Genre, BookInstance
from catalog.forms import AuthorsForm

class BookCreate(CreateView):
    model = Book 
    fields = '__all__'
    def get_success_url(self):
        return reverse_lazy('books')
    
class BookUpdate(UpdateView):
    model = Book 
    fields = '__all__'
    def get_success_url(self):
        return reverse_lazy('books')    

class BookDelete(DeleteView):
    model = Book 
    def get_success_url(self):
        return reverse_lazy('books')        

def create(request):
    if request.method == 'POST':
        author = Author.objects.create(
            first_name = request.POST.get('first_name'),
            last_name = request.POST.get('last_name'),
            date_of_birth = request.POST.get('date_of_birth'),
            date_of_death = request.POST.get('date_of_death'),
        )
        return HttpResponseRedirect('/authors_add/')
        
def edit1(request, id):
    author = Author.objects.get(id = id)
    if request.method == 'POST':
        author.first_name = request.POST.get('first_name')
        author.last_name = request.POST.get('last_name')
        author.date_of_birth = request.POST.get('date_of_birth')
        author.date_of_death = request.POST.get('date_of_death')
        author.save()
        return HttpResponseRedirect('/authors_add/')
    else:
        return render(request, 'edit1.html', {'author': author})    

def delete(request, id):
    try:
        author = Author.objects.get(id = id)
        author.delete()
        return HttpResponseRedirect('/authors_add/')
    except Author.DoesNotExist:
        return HttpResponse('<h2>Muallif topilmadi</h2>')

def authors_add(request):
    authors = Author.objects.all()
    authorsform = AuthorsForm()
    return render(request, 'catalog/authors_add.html', {'form': authorsform, 'authors': authors})

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance 
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 3
    
    def get_queryset(self):
        return BookInstance.objects.filter(
            borrower = self.request.user
        ).filter(status__exact = 2).order_by('due_back')
    

def index(request):
    if not request.user.is_authenticated:
        return redirect(f'/accounts/login/?next={request.path}')
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Omborda bo'lgan kitob nusxalari sonini topish
    num_instances_available = BookInstance.objects.filter(status__exact = 2).count()
    num_authors = Author.objects.all().count()
    
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    return render(request, 'index.html', {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,    
    })
    
class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    paginate_by = 3

class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book
    
class AuthorsListView(LoginRequiredMixin, generic.ListView):
    model = Author
    paginate_by = 3
 