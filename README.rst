Elasticsearch Watcher
=====================

This is an addon to the official elasticsearch python client that adds
functionality for the Watcher plugin. 

Installation
------------

You can install this addon using ``pip``::

    pip install elasticsearch-watcher

Usage
-----

You can use this client alone::

    from elasticsearch import Elasticsearch
    from elasticsearch_watcher import WatcherClient

    client = Elasticsearch()
    watcher = WatcherClient(client)

    watcher.get_watch(id=42)

Or you can add the ``watcher`` namespace to the official client to mimic the
behaviors of other namespaces::

    WatcherClient.infect_client(client)

    client.watcher.get_watch(id=42)

Complex example
---------------

A more comprehensive example::

    from time import sleep
    from datetime import datetime
    from random import randint

    from elasticsearch import Elasticsearch
    from elasticsearch_watcher import WatcherClient

    # initialize the standard client as usual
    es = Elasticsearch()
    # add the .watcher namespace to it
    WatcherClient.infect_client(es)

    # clear the index fiorst
    es.indices.delete(
        index=['alerts', 'test', '.watches', '.watch_history*'], ignore=404)

    # get the watcher plugin version
    print('Using watcher', es.watcher.info()['version']['number'])

    # Register a new watch
    es.watcher.put_watch(
        id='error_500',
        body={
            # label the watch
            'metadata': {'tags': ['errors']},

            # Run the watch every 10 seconds
            'trigger': { 'schedule': { 'interval': '10s' } },
    
            # Search for at least 3 documents matching the condition
            'condition': {  'script': { 'inline': 'ctx.payload.hits.total > 3' } },
    
            # Throttle the watch execution for 30 seconds
            'throttle_period': '30s',
    
            # The search request to execute
            'input':   {
                'search': {
                    'request': {
                        'indices': ['test'],
                        'body': {
                            'query': {
                                'filtered': {
                                    'query': { 'match': { 'status': 500 } },
                                    'filter': { 'range': { 'timestamp': { 'from': '{{ctx.trigger.scheduled_time}}||-5m', 'to': '{{ctx.trigger.triggered_time}}' } } }
                                }
                            },
                            # Return statistics about different hosts
                            'aggregations': {
                                'hosts': { 'terms': { 'field': 'host' } }
                            }
            }}}},
    
            # The actions to perform
            'actions': {
                'send_email':    {
                    'transform': {
                        # Transform the data for the template
                        'script': '''return [
                                total: ctx.payload.hits.total,
                                hosts: ctx.payload.aggregations.hosts.buckets.collect { [ host: it.key, errors: it.doc_count ] },
                                errors: ctx.payload.hits.hits.collect { it._source } 
                            ];'''
                    },
                    'email': {
                        'to': 'you@example.com',
                        'subject': '[ALERT] {{ctx.watch_id}}',
                        'attach_data': True,
                        'body':  '''
                            Received {{ctx.payload.total}} error documents in the last 5 minutes.

                            Hosts:

                            {{#ctx.payload.hosts}}* {{host}} ({{errors}})
                            {{/ctx.payload.hosts}}'''.replace('\n'+' '*24, '\n').strip(),
                    }
                },
                'index_payload': {
                    # Transform the data to be stored
                    'transform': { 'script': 'return [ watch_id: ctx.watch_id, payload: ctx.payload ]' },
                    'index': { 'index': 'alerts', 'doc_type': 'alert' }
                },
                'ping_webhook': {
                    'webhook': {
                        'method': 'POST',
                        'host': 'localhost',
                        'port': 8000,
                        'path': '/',
                        'body': '{"watch_id" : "{{ctx.watch_id}}", "payload" : "{{ctx.payload}}"}'
                    }
                }
            }
        }
    )

    # index documents to trigger the watch
    for _ in range(5):
        es.index(
            index='test',
            doc_type='d',
            body={
                'timestamp': datetime.utcnow(),
                'status': 500,
                'host': '10.0.0.%d' % randint(1, 3)
            }
        )

    # wait a bit...
    for _ in range(30):
        sleep(1)
        print('.', sep='', end='', flush=True)
    print()

    # display information about watch execution
    print('=' * 80)
    s = es.search(
        index='.watch_history*',
        q='watch_id:error_500',
        sort='trigger_event.schedule.triggered_time:asc'
    )
    for hit in s['hits']['hits']:
        print('%s: %s' % (hit['_id'], hit['_source']['state']))

    # delete the watch
    es.watcher.delete_watch(id='error_500', force=True)


License
-------

Copyright 2015 Elasticsearch

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

