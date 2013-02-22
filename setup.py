#!/usr/bin/env python

import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="rapidsms-telerivet",
    version="0.0.1",
    description="A Telerivet SMS backend for RapidSMS",
    long_description=read('README.rst'),
    author="TimbaObjects",
    author_email="info@timbaobjects.com",
    url="http://github.com/timbaobjects/rapidsms-telerivet/",
    packages=['rapidsms_telerivet'],
    )
