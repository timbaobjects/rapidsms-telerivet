rapidsms-telerivet
==================

A Telerivet backend for RapidSMS. With rapidsms-telerivet, your RapidSMS deployment can process incoming messages and send out responses using your Telerivet account.

`Telerivet`_ is a web-based service that enables you to create SMS services using smartphones and other online SMS gateways.

.. _Telerivet: http://telerivet.com/

Installing
==========

Here's how to install rapidsms-telerivet:

::

  $ pip install git+https://github.com/timbaobjects/rapidsms-telerivet.git#egg=rapidsms-telerivet

Usage
=====

The first step is to configure a url for the backend in your ``urls.py``:

::

  from rapidsms_telerivet.views import TelerivetBackendView

  urlpatterns += patterns('',
    (r'^telerivet/', TelerivetBackendView.as_view(backend_name='telerivet')),
  )

Secondly, just like every RapidSMS backend, you need to configure this in your ``settings.py``:

::

  INSTALLED_BACKENDS = {
    "telerivet": {
        "ENGINE": "rapidsms_telerivet.outgoing.TelerivetBackend",
        "project_id": "your telerivet project id",
        "phone_id": "phone id for one of the devices attached to your telerivet account",
        "secret": "the webhook trigger secret from telerivet",
        "api_key": "telerivet api key"
    }
  }

Bugs?
=====

Discover any bugs or have any other feature requests? Feel free to submit it on the `issue tracker`_

.. _issue tracker: https://github.com/timbaobjects/rapidsms-telerivet/issues
