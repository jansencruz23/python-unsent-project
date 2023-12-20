from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Letter


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = 'User Name'
        self.fields['username'].help_text = ''

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = 'Password'
        self.fields['password1'].help_text = ''

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = 'Confirm Password'
        self.fields['password2'].help_text = ''


class AddLetterForm(forms.ModelForm):
    recipient = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder':'Recipient', 'class':'form-control'}), label='')
    message = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder':'Message', 'class':'form-control'}), label='')
    letter_color = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder':'Letter Color', 'class':'form-control'}), label='')
    is_visible = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'form-check-input'}), label='Is Visible')

    class Meta:
        model = Letter
        exclude = ('user',)

