from django.test import TestCase

# Create your tests here.
from django import forms

class AgentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        keys = kwargs.pop('keys', [])
        super().__init__(*args, **kwargs)
        # Set dynamic choices for selector_key including the initial placeholder
        self.fields['selector_key'].choices = [('', 'choose your key')] + [
            (key.id, key.name) for key in keys
        ]

    # Text Input Fields
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'bord-bottom focus:outline-0 w-72',
            'placeholder': 'name',
        }),
        required=True
    )

    LLM = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'bord-bottom focus:outline-0 w-72',
            'placeholder': 'LLM name',
        }),
        required=True
    )

    job = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'bord-bottom focus:outline-0 w-72',
            'placeholder': 'job title',
        }),
        required=True
    )

    company_url = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'bord-bottom focus:outline-0 w-72',
            'placeholder': 'company url',
        }),
        required=True
    )

    objective = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'bord-bottom focus:outline-0 w-72 justify-self-center',
            'placeholder': 'company objective',
        }),
        required=True
    )

    # Checkboxes
    memory = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            'class': 'checkbox checkbox-secondary',
        }),
        required=False
    )

    compress = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            'class': 'checkbox checkbox-secondary',
        }),
        required=False
    )

    answers = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            'class': 'checkbox checkbox-secondary',
        }),
        required=False
    )

    # Select Dropdown
    selector_key = forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'text-xs outline-0 focus:outline-0 min-h-max max-h-min w-48',
        }),
        choices=[],  # Will be populated in __init__
        required=True
    )