import urllib
import urllib2
import base64

from rapidsms.backends.base import BackendBase


class TelerivetBackend(BackendBase):
    """Backend for use with the Telerivet SMS Service."""

    def configure(self, phone_id, project_id, api_key, rest_endpoint='https://api.telerivet.com/v1/projects/{}/messages/outgoing',
                  **kwargs):
        self.rest_endpoint = rest_endpoint.format(project_id)
        self.phone_id = phone_id
        self.api_key = api_key

    def prepare_message(self, message):
        """Prepare URL query string with message context."""
        query = {
            'to_number': message.connection.identity,
            'content': message.text,
            'phone_id': self.phone_id
        }
        return query

    def send(self, message):
        """Open request to Telerivet."""
        self.info('Sending message: %s' % message)
        url_args = self.prepare_message(message)
        data = urllib.urlencode(url_args)
        try:
            self.debug('Opening URL: %s' % self.rest_endpoint)
            req = urllib2.Request(self.rest_endpoint)
            # Telerivet requires basic authentication using the api_key as username
            # and anything as the password
            basic_auth = base64.encodestring('{}:{}'.format(self.api_key, '*****')).replace('\n', '')
            req.add_data(data)
            req.add_header("Authorization", "Basic {}".format(basic_auth))
            response = urllib2.urlopen(req)
        except:
            self.exception('Failed to send message')
            return
        self.info('SENT')
        self.debug('response body: %s' % response.read())
        return True
