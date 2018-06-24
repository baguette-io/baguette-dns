#-*- coding:utf-8 -*-
"""
Unit tests for the service module.
"""
#pylint:disable=wildcard-import,unused-wildcard-import,redefined-outer-name,unused-argument,invalid-name,line-too-long
from .fixtures import *

def test_create_record_ok(levain):
    """
    Try to create a record while powerdns is ok:
    must succeed.
    """
    result = mock.Mock(return_value={'status':0})
    with mock.patch('sel.request.Request.request', result) as m:
        assert levain.create_record({'domain':'test.projects.baguette.io'}, mock.Mock()) is True
    assert m.call_count == 1
    m.assert_called_once_with('servers/localhost/zones/projects.baguette.io', __method__='patch', json={'rrsets': [{'records': [{'content': 'xxxx.elb.amazonaws.com', 'disabled': False}], 'changetype': 'REPLACE', 'type': 'CNAME', 'name': 'test.projects.baguette.io.', 'ttl': 60}]}, headers={'X-API-Key': 'MyPowerDNSKey'})


def test_create_invalid_domain(levain):
    """
    Try to create a record that is invalid:
    must fails.
    """
    result = mock.Mock(return_value={'status':0})
    with mock.patch('sel.request.Request.request', result) as m:
        assert levain.create_record({'domain':'www.baguette.io'}, mock.Mock()) is False
    assert m.call_count == 0

def test_create_dns_ko(levain):
    """
    Try to create a record while powerdns is ko:
    must fails.
    """
    result = mock.Mock(return_value={'status':-1})
    with mock.patch('sel.request.Request.request', result) as m:
        assert levain.create_record({'domain':'test.projects.baguette.io'}, mock.Mock()) is False
    assert m.call_count == 1
