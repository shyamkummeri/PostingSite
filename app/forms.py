from django import forms
from app.models import UserRegister
import re

class UserRegisterForm(forms.ModelForm):

    userName = forms.CharField(label='User Name')
    emailId = forms.EmailField(label='Email Id')
    contactNumber = forms.CharField(label='Contact Number')
    password = forms.CharField(widget=forms.PasswordInput,label='Password')

    class Meta:
        model = UserRegister
        fields = '__all__'
    def clean_contactNumber(self):
        c = self.cleaned_data["contactNumber"]
        r = re.findall(r'^[0-9]*$', c)
        if r:
            return r[0]
        else:
            raise forms.ValidationError('Please Enter Contact Number 0-9')

