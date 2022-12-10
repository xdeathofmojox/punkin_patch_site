from django import forms
from .models import PatchTemplate, Character
from django.core.exceptions import ValidationError

class RequestFormMixin:
    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super().get_form_kwargs(*args, **kwargs)
        form_kwargs['request'] = self.request
        return form_kwargs

class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ["name", "image"]

class PatchForm(forms.ModelForm):
    class Meta:
        model = PatchTemplate
        fields = ["characters", "name"]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(PatchForm, self).__init__(*args, **kwargs)
        self.fields["characters"].queryset = Character.objects.filter(user=self.request.user)

    def clean(self):
        characters = self.cleaned_data.get('characters')
        user = self.request.user
        if characters and user:
            for character in characters:
                if user != character.user:
                    raise ValidationError("User: {} does not have permissions".format(user))
        return self.cleaned_data