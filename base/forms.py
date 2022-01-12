from django import forms
from django.forms import ModelForm, widgets

from .models import Userprofile, Weathertype, Location

# https://docs.djangoproject.com/en/3.2/topics/forms/
class EventForm(forms.Form):
    weathertypeid = forms.MultipleChoiceField(
        label='Weather Type',
        required=False,
        widget = forms.Select(choices=['',''])
    )
    locationid = forms.MultipleChoiceField(
        label='Location',
        required=False,
        widget = forms.Select(choices=['',''])
    )
    eventdate = forms.DateField(
        label='Event Date',
        required=False,
        widget=forms.SelectDateWidget(years=[2020,2021])
    )
    severity = forms.CharField(
        label='Severity',
        required=False,
        max_length=16,
        widget = forms.Select(choices=[('None', 'All'), ('Light', 'Light'), ('Moderate', 'Moderate'), ('Heavy', 'Heavy'), ('Severe', 'Severe'), ('UNK', 'UNK'), ('Other', 'Other')])
    )

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        w_c = [(w.id, w.typename) for w in Weathertype.objects.all()]
        w_c.insert(0, ('None', 'All'))
        self.fields['weathertypeid'].widget = forms.Select(choices=w_c)
        l_c = [(l.id, str(l)) for l in Location.objects.all()]
        l_c.insert(0, ('None', 'All'))
        self.fields['locationid'].widget = forms.Select(choices=l_c)

# https://docs.djangoproject.com/en/3.2/topics/forms/modelforms/
class ProfileForm(ModelForm):
    # TODO: implement validation

    class Meta:
        model = Userprofile
        fields = ('name', 'timezone', 'locationid')
        labels = {
            'name': 'Displayed Name',
            'timzone': 'Timezone (UTC)',
            'locationid': 'Location'
        }
        # widgets = {
        #     'timezone' : forms.Select(choices=[(i, i - 12) for i in range(27)]),
        # }