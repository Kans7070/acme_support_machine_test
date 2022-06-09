from pyexpat import model
from django import forms
from apps.custom_admin.models import Department
from apps.user.models import User

class CreateUserForm(forms.ModelForm):
    name = forms.CharField( widget=forms.TextInput(attrs={
        'class': 'form-control col-6 mb-3',
        'placeholder':'name',
        }),label='')

    email = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control col-5 mb-3',
        'placeholder':'email',
        }),label='')
    
    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control col-6 mb-3',
        "oninput": "this.value = this.value.replace(/[^0-9]/g, '').replace(/(\..*)\./g, '$1');",
        "maxlength": "10",
        'placeholder':'phone_number',
        }),label='')
    department = forms.ModelChoiceField(widget=forms.Select(attrs={
        'class': 'form-control col-2 mb-3',
        'placeholder':'department',
    }),label='',queryset=Department.object.all())

    
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control col-5 mb-3',
        'placeholder':'password',
        }),label='')
    
    

    class Meta:
        model=User
        fields=['name','email','phone_number','password','department']
    


class CreateDepartmentForm(forms.ModelForm):
    name = forms.CharField( widget=forms.TextInput(attrs={
        'class': 'form-control col-6 mb-3',
        'placeholder':'name',
        
        }),label='')

    description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control col-12 mb-3',
        'placeholder':'description',
        'rows':'5'
        }),label='')
    
    class Meta:
        model=Department
        fields=['name','description',]
    