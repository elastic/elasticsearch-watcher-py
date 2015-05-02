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

