from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import PatchTemplate
from .forms import PatchForm, RequestFormMixin
from django.urls import reverse_lazy

class PatchForUserMixin:
    def get_queryset(self):
        return PatchTemplate.objects.filter(user=self.request.user)

    def create(self, data):
        return PatchTemplate.objects.filter(user=self.request.user, **data)

class PatchList(PatchForUserMixin, LoginRequiredMixin, ListView):
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


class PatchDetail(PatchForUserMixin, LoginRequiredMixin, DetailView):
    model = PatchTemplate
    context_object_name = 'patch'
    template_name = 'punkin_patch/patches/patch.html'

class PatchCreate(RequestFormMixin, PatchForUserMixin, LoginRequiredMixin, CreateView):
    model = PatchTemplate
    form_class = PatchForm
    success_url = reverse_lazy('patches')
    template_name = 'punkin_patch/patches/patch_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PatchCreate, self).form_valid(form)


class PatchUpdate(RequestFormMixin, PatchForUserMixin, LoginRequiredMixin, UpdateView):
    model = PatchTemplate
    form_class = PatchForm
    success_url = reverse_lazy('patches')
    template_name = 'punkin_patch/patches/patch_form.html'


class PatchDelete(PatchForUserMixin, LoginRequiredMixin, DeleteView):
    model = PatchTemplate
    context_object_name = 'patch'
    success_url = reverse_lazy('patches')
    template_name = 'punkin_patch/patches/patch_confirm_delete.html'