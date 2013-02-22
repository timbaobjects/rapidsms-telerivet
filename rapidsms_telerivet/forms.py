from django import forms
from django.conf import settings

from rapidsms.backends.http.forms import BaseHttpForm


class TelerivetForm(BaseHttpForm):
    event = forms.CharField(required=False)
    id = forms.CharField(required=False)
    message_type = forms.CharField(required=False)
    from_number = forms.CharField()
    contact_id = forms.CharField(required=False)
    phone_id = forms.CharField(required=False)
    to_number = forms.CharField(required=False)
    time_created = forms.CharField(required=False)
    content = forms.CharField()
    project_id = forms.CharField(required=False)
    secret = forms.CharField(required=False)

    def clean_secret(self):
        secret = self.cleaned_data['secret']
        if secret != settings.INSTALLED_BACKENDS[self.backend_name].get('secret', None):
            raise forms.ValidationError('Incorrect secret')
        return secret

    def get_incoming_data(self):
        connections = self.lookup_connections([self.cleaned_data['from_number']])
        return {'connection': connections[0],
                'text': self.cleaned_data['content']}
