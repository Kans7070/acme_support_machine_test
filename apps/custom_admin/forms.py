import json
from django import forms
from apps.custom_admin.models import Department
from apps.user.models import User
from apps.zdesk import create_ticket


class CreateUserForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control col-5 mb-3',
        'placeholder': 'name',
    }), label='')

    email = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control col-5 mb-3',
        'placeholder': 'email',
    }), label='')

    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control col-5 mb-3',
        "oninput": "this.value = this.value.replace(/[^0-9]/g, '').replace(/(\..*)\./g, '$1');",
        "maxlength": "10",
        'placeholder': 'phone_number',
    }), label='')

    department = forms.ModelChoiceField(widget=forms.Select(attrs={
        'class': 'form-control col-4 mb-3',
        'placeholder': 'department',
    }), label='', queryset=Department.object.all())

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control col-5 mb-3',
        'placeholder': 'password',
    }), label='')

    class Meta:
        model = User
        fields = ['name', 'email', 'phone_number', 'password', 'department']


class CreateDepartmentForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control col-6 mb-3',
        'placeholder': 'name',

    }), label='')

    description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control col-12 mb-3',
        'placeholder': 'description',
        'rows': '5'
    }), label='')

    class Meta:
        model = Department
        fields = ['name', 'description', ]

    def save(self):
        self.instance.name = self.instance.name.upper()
        
        self.instance.save()


class TicketForm(forms.Form):

    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    )

    subject = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control col-6 mb-3',
        'placeholder': 'subject',

    }), label='')
    
    description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control col-12 mb-3',
        'placeholder': 'description',
        'rows': '5'
    }), label='')

    priority = forms.ChoiceField(choices=PRIORITY_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control col-4 mb-3',
        'placeholder': '',
    }), label='priority')

    class Meta:
        fields = ['subject', 'description', 'priority']

    def save(self, data):
        create_ticket(data)
