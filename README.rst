============
baguette-dns
============

Little DNS service that will create/delete dns records.

Configuration
=============

Define the **/etc/farine.ini** or override the path using the environment variable **FARINE_INI**:

::

    [DEFAULT]
    amqp_uri=amqp://127.0.0.1:5672/amqp

    [levain]
    dns_api=http://127.0.0.1:8081/api/v1/
    dns_key=MyPowerDNSKey
    dns_root=projects.baguette.io
    public_cname=xxxx.elb.amazonaws.com


Launch
======

::

    farine --start=levain

OpenDNS
=======

Create a zone
-------------

::

    curl -X POST --data '{"name":"example.org.", "kind": "Native", "masters": [], "nameservers": ["ns1.example.org.", "ns2.example.org."]}' -H 'X-API-Key: admin' http://127.0.0.1:8081/api/v1/servers/localhost/zones | jq


List all zones
--------------

::

    curl -H 'X-API-Key: admin' http://127.0.0.1:8081/servers/localhost/zones

Show a specifif zone
--------------------

::

    curl -H 'X-API-Key: admin' http://127.0.0.1:8081/api/v1/servers/localhost/zones/example.org. | jq


Add/Update a record
-------------------

**rrset** means *Resource Record Set*

::

    curl -X PATCH --data '{"rrsets": [ {"name": "test.example.org.", "type": "A", "ttl": 60, "changetype": "REPLACE", "records": [ {"content": "192.0.5.4", "disabled": false } ] } ] }' -H 'X-API-Key: admin' http://127.0.0.1:8081/api/v1/servers/localhost/zones/example.org. | jq


Delete a record
---------------

::

    curl -X PATCH --data '{"rrsets": [ {"name": "test.example.org.", "type": "A", "changetype": "DELETE" } ] }' -H 'X-API-Key: admin' http://127.0.0.1:8081/api/v1/servers/localhost/zones/example.org. | jq
