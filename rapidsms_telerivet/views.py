from django.http import HttpResponse

from rapidsms_telerivet.forms import TelerivetForm
from rapidsms.backends.http.views import BaseHttpBackendView


class TelerivetBackendView(BaseHttpBackendView):
    """Backend view for handling inbound SMSes from Telerivet."""

    http_method_names = ['post']
    form_class = TelerivetForm

    def form_valid(self, form):
        super(TelerivetBackendView, self).form_valid(form)
        # there isn't any need to send a response here
        return HttpResponse('')
