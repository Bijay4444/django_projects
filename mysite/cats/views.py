from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from . models import Cat, Breed


class MainView(LoginRequiredMixin, View):
    def get(self, request):
        bc = Breed.objects.count()
        cat= Cat.objects.all()

        context = {'breed_count': bc, 'cat_list': cat}
        return render(request, 'cats/cat_list.html',context)

# Cat CRUD.

class CatCreate(LoginRequiredMixin, CreateView):
    model = Cat
    fields = '__all__'
    success_url = reverse_lazy("cats:all")

class CatUpdate(LoginRequiredMixin, UpdateView):
    model = Cat
    fields = '__all__'
    success_url = reverse_lazy("cats:all")

class CatDelete(LoginRequiredMixin, DeleteView):
    model = Cat
    fields = '__all__'
    success_url = reverse_lazy("cats:all")

#Breed CRUD

class BreedList(LoginRequiredMixin, ListView):
    model = Breed

class BreedCreate(LoginRequiredMixin, CreateView):
    model = Breed
    fields = '__all__'
    success_url = reverse_lazy("cats:all")

class BreedUpdate(LoginRequiredMixin, UpdateView):
    model = Breed
    fields ='__all__'
    success_url = reverse_lazy("cats:all")

class BreedDelete(LoginRequiredMixin, DeleteView):
    model = Breed
    success_url = reverse_lazy("cats:all")