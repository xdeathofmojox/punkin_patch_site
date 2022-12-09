from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Character
from django.urls import reverse_lazy

class CharacterList(LoginRequiredMixin, ListView):
    model = Character
    context_object_name = 'characters'
    template_name = 'punkin_patch/characters/character_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['characters'] = context['characters'].filter(user=self.request.user)

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['characters'] = context['characters'].filter(
                name__contains=search_input)

        context['search_input'] = search_input

        return context


class CharacterDetail(LoginRequiredMixin, DetailView):
    model = Character
    context_object_name = 'character'
    template_name = 'punkin_patch/characters/character.html'


class CharacterCreate(LoginRequiredMixin, CreateView):
    model = Character
    fields = ['name']
    success_url = reverse_lazy('characters')
    template_name = 'punkin_patch/characters/character_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CharacterCreate, self).form_valid(form)


class CharacterUpdate(LoginRequiredMixin, UpdateView):
    model = Character
    fields = ['name']
    success_url = reverse_lazy('characters')
    template_name = 'punkin_patch/characters/character_form.html'


class CharacterDelete(LoginRequiredMixin, DeleteView):
    model = Character
    context_object_name = 'character'
    success_url = reverse_lazy('characters')
    template_name = 'punkin_patch/characters/character_confirm_delete.html'
    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)