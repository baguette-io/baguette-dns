#-*- coding:utf-8 -*-
#pylint:disable=unsubscriptable-object
"""
| Module DNS
| which will create/delete a DNS entry
| when an user is pushing to a branch.

|The operations are idempotent.
"""
import logging
import os
import farine.amqp
import farine.settings
import sel

LOGGER = logging.getLogger(__name__)

class Levain(object):
    """
    Service which contains the event loops to manage the DNS workflow:
    * delete-record
    * create-record
    """
    @farine.amqp.consume(exchange='dns', routing_key='delete-record')
    def delete_record(self, body, message):
        """
        Listen to the `exchange` dns
        | and delete the dns entry accordly to the messages.
        | Idempotent.
        :param body: the dns name to delete.
        :type body: dict
        :param message: The raw message.
        :type message: kombu.message.Message
        :rtype: bool
        """
        message.ack()
        return True

    @farine.amqp.consume(exchange='dns', routing_key='create-record')
    def create_record(self, body, message):
        """
        Listen to the `exchange` dns,
        | and create the dns entry accordly to the messages.
        | Idempotent.

        :param body: The message's content.
        :type body: dict
        :param message: The dns to create.
        :type message: kombu.message.Message
        :returns: The creation state
        :rtype: bool
        """
        settings = farine.settings.levain
        #1. Check the domain is valid
        if not body['domain'].endswith(settings['dns_root']):
            LOGGER.info('domain %s is not a subdomain of %s',
                        body['domain'], settings['dns_root'])
            return False
        #2. Format data to send
        data = {
            "rrsets": [{
                "name": "{}.".format(body['domain']),
                "type": "CNAME",
                "ttl": 60,
                "changetype": "REPLACE",
                "records": [{"content": "{}.".format(settings['public_cname']), "disabled": False}]
            }]
        }
        #3. Send
        request = sel.Request(settings['dns_api'])
        headers = {'X-API-Key' : settings['dns_key']}
        endpoint = os.path.join('servers/localhost/zones/', settings['dns_root'])
        response = request.patch(endpoint, json=data, headers=headers)
        if response['status'] != 0:
            LOGGER.error('Cannot update domain %s', body['domain'])
            return False
        message.ack()
        return True
