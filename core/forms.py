from django import forms
from core.utils import sda_login


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Email / Username', widget=forms.TextInput(
            attrs={'placeholder': 'Ex. alex@tailbyte.org', 'class': 'input input-bordered w-full'}))
    password = forms.CharField(
        label='Password', widget=forms.PasswordInput(
            attrs={'placeholder': '••••••••', 'class': 'input input-bordered w-full'}))

    def login(self):
        success, userdata = sda_login(self.cleaned_data.get('username'), self.cleaned_data.get('password'))
        print(userdata)
