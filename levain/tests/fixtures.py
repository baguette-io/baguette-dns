#-*- coding:utf-8 -*-
#pylint:disable=missing-docstring,unused-import,no-member,line-too-long,no-name-in-module,redefined-outer-name
import collections
import random
import string
import mock
import pytest
import farine.settings
from farine.tests.fixtures import amqp_factory, message_factory, queue_factory

@pytest.fixture(autouse=True)
def settings():
    """
    auto load the settings.
    """
    farine.settings.load()

@pytest.fixture()
def levain():
    """
    dns service fixture.
    """
    import levain.service
    return levain.service.Levain()
