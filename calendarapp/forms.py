from django.forms import ModelForm, DateInput
from calendarapp.models import Event, EventMember
from django import forms


class EventForm(forms.ModelForm):
  class Meta:
    model = Event
    fields = "__all__"
    exclude = ['user']
    widgets = {
      'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
      'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
    }
    

  def __init__(self, *args, **kwargs): #parse the for input datatime form
    super(EventForm, self).__init__(*args, **kwargs)
    self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
    self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)



class EventMemberForm(forms.ModelForm):
  class Meta:
    model = EventMember
    fields = ['user']

class SigninForm(forms.Form):
  username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
  password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


# class SignupForm(forms.Form):
#   username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
#   password = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
