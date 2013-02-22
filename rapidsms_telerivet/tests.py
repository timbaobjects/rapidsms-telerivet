from django.test import TestCase
from django.core.urlresolvers import reverse
from django.conf.urls.defaults import *

from rapidsms_telerivet import views
from rapidsms_telerivet.outgoing import TelerivetBackend
from rapidsms_telerivet.forms import TelerivetForm
from rapidsms.tests.harness import RapidTest, CreateDataMixin


urlpatterns = patterns('',
                       url(r"^backend/telerivet/$",
                           views.KannelBackendView.as_view(
                               backend_name='telerivet-backend'),
                           name='telerivet-backend'),
                       )


class TelerivetFormTest(TestCase):

    def test_valid_form(self):
        """Form should be valid if GET keys match configuration."""
        data = {'from_number': '1112223333', 'content': 'hi there'}
        form = TelerivetForm(data, backend_name='telerivet-backend')
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        """Form is invalid if POST keys don't match configuration."""
        data = {'invalid-phone': '1112223333', 'invalid-message': 'hi there'}
        form = TelerivetForm(data, backend_name='telerivet-backend')
        self.assertFalse(form.is_valid())

    def test_get_incoming_data(self):
        """get_incoming_data should return matching text and connection."""
        data = {'from_number': '1112223333', 'content': 'hi there'}
        form = TelerivetForm(data, backend_name='telerivet-backend')
        self.assertTrue(form.is_valid())
        incoming_data = form.get_incoming_data()
        self.assertEqual(data['content'], incoming_data['text'])
        self.assertEqual(data['from_number'],
                         incoming_data['connection'].identity)
        self.assertEqual('telerivet-backend',
                         incoming_data['connection'].backend.name)


class TelerivetViewTest(RapidTest):

    urls = 'telerivet.tests'
    disable_phases = True

    def test_valid_response_get(self):
        """HTTP 200 should return if data is valid."""
        data = {'from_number': '1112223333', 'content': 'hi there'}
        response = self.client.get(reverse('telerivet-backend'), data)
        self.assertEqual(response.status_code, 200)

    def test_invalid_response(self):
        """HTTP 400 should return if data is invalid."""
        data = {'invalid-phone': '1112223333', 'message': 'hi there'}
        response = self.client.get(reverse('telerivet-backend'), data)
        self.assertEqual(response.status_code, 400)

    def test_valid_post_message(self):
        """Valid POSTs should pass message object to router."""
        data = {'from_number': '1112223333', 'content': 'hi there'}
        self.client.get(reverse('telerivet-backend'), data)
        message = self.inbound[0]
        self.assertEqual(data['content'], message.text)
        self.assertEqual(data['from_number'],
                         message.connection.identity)
        self.assertEqual('telerivet-backend',
                         message.connection.backend.name)


class TelerivetSendTest(CreateDataMixin, TestCase):

    def test_outgoing_keys(self):
        """Outgoing POST data should contain the proper keys."""
        message = self.create_outgoing_message()
        config = {
            "project_id": "1",
            "rest_endpoint": 'https://api.telerivet.com/v1/projects/{}/messages/outgoing',
            "phone_id": "1"
        }
        backend = TelerivetBackend(None, "telerivet", **config)
        data = backend.prepare_message(message)
        self.assertEqual(config['phone_id'], data['phone_id'])
        self.assertEqual(message.connection.identity, data['to_number'])
        self.assertEqual(message.text, data['content'])
