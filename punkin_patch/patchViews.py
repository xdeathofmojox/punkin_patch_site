from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import PatchTemplate
from django.urls import reverse_lazy

class PatchList(LoginRequiredMixin, ListView):
    model = PatchTemplate
    context_object_name = 'patches'
    template_name = 'punkin_patch/patches/patch_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patches'] = context['patches'].filter(user=self.request.user)

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['patches'] = context['patches'].filter(
                name__contains=search_input)

        context['search_input'] = search_input

        return context


class PatchDetail(LoginRequiredMixin, DetailView):
    model = PatchTemplate
    context_object_name = 'patch'
    template_name = 'punkin_patch/patches/patch.html'


class PatchCreate(LoginRequiredMixin, CreateView):
    model = PatchTemplate
    fields = ['name']
    success_url = reverse_lazy('patches')
    template_name = 'punkin_patch/patches/patch_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PatchCreate, self).form_valid(form)


class PatchUpdate(LoginRequiredMixin, UpdateView):
    model = PatchTemplate
    fields = ['name']
    success_url = reverse_lazy('patches')
    template_name = 'punkin_patch/patches/patch_form.html'


class PatchDelete(LoginRequiredMixin, DeleteView):
    model = PatchTemplate
    context_object_name = 'patch'
    success_url = reverse_lazy('patches')
    template_name = 'punkin_patch/patches/patch_confirm_delete.html'
    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)