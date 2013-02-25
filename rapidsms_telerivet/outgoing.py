import requests
from requests.auth import HTTPBasicAuth

from rapidsms.backends.base import BackendBase


class TelerivetBackend(BackendBase):
    """Backend for use with the Telerivet SMS Service."""

    def configure(self, phone_id, project_id, api_key, rest_endpoint='https://api.telerivet.com/v1/projects/{}/messages/outgoing',
                  **kwargs):
        self.rest_endpoint = rest_endpoint.format(project_id)
        self.phone_id = phone_id
        self.api_key = api_key

    def prepare_message(self, message=None, id_=None, text=None, identities=None, context=None):
        """Prepare URL query string with message context."""
        if message:
            query = {
                'to_number': message.connection.identity,
                'content': message.text,
                'phone_id': self.phone_id
            }
        else:
            # unfortunately at this time, we can only send to one
            # phone number using the REST API at a time
            query = {
                'to_number': identities[0] if isinstance(identities, list) else identities,
                'content': text,
                'phone_id': self.phone_id
            }

        return query

    def send(self, message=None, id_=None, text=None, identities=None, context=None):
        """Open request to Telerivet."""
        if message:
            self.info('Sending message: %s' % message)
            url_args = self.prepare_message(message)
            try:
                self.debug('Opening URL: %s' % self.rest_endpoint)
                response = requests.post(self.rest_endpoint, data=url_args, auth=HTTPBasicAuth(self.api_key, ''))
            except:
                self.exception('Failed to send message')
                return
        else:
            self.info('Sending message: %s' % text)
            for identity in identities:
                url_args = self.prepare_message(id_=id_, text=text, identities=identity, context=context)
                try:
                    self.debug('Opening URL: %s' % self.rest_endpoint)
                    response = requests.post(self.rest_endpoint, data=url_args, auth=HTTPBasicAuth(self.api_key, ''))
                except:
                    self.exception('Failed to send message')
                    return
        self.info('SENT')
        self.debug('response body: %s' % response)
        return True
