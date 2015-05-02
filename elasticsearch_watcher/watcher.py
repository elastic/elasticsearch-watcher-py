from elasticsearch.utils import AddonClient, query_params, _make_path, SKIP_IN_PATH

class WatcherClient(AddonClient):
    @query_params()
    def info(self, params=None):
        """
        `<http://www.elastic.co/guide/en/watcher/current/appendix-api-info.html>`_
        """
        _, data = self.transport.perform_request('GET', '/_watcher/',
            params=params)
        return data

    @query_params('pretty')
    def put_watch(self, id, body, params=None):
        """
        `<http://www.elastic.co/guide/en/watcher/current/appendix-api-put-watch.html>`_

        :arg id: Watch ID
        :arg body: The watch
        :arg pretty: Pretty the output, default False
        """
        for param in (id, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")
        _, data = self.transport.perform_request('PUT', _make_path('_watcher',
            'watch', id), params=params, body=body)
        return data

    @query_params()
    def stats(self, params=None):
        """
        `<http://www.elastic.co/guide/en/watcher/current/appendix-api-stats.html>`_
        """
        _, data = self.transport.perform_request('GET', '/_watcher/stats',
            params=params)
        return data

    @query_params()
    def stop(self, params=None):
        """
        `<http://www.elastic.co/guide/en/watcher/current/appendix-api-service.html>`_
        """
        _, data = self.transport.perform_request('PUT', '/_watcher/_stop',
            params=params)
        return data

    @query_params()
    def start(self, params=None):
        """
        `<http://www.elastic.co/guide/en/watcher/current/appendix-api-service.html>`_
        """
        _, data = self.transport.perform_request('PUT', '/_watcher/_start',
            params=params)
        return data

    @query_params()
    def ack_watch(self, id, params=None):
        """
        `<http://www.elastic.co/guide/en/watcher/current/appendix-api-ack-watch.html>`_

        :arg id: Watch ID
        """
        if id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'id'.")
        _, data = self.transport.perform_request('PUT', _make_path('_watcher',
            'watch', id, '_ack'), params=params)
        return data

    @query_params()
    def execute_watch(self, id, body=None, params=None):
        """
        `<http://www.elastic.co/guide/en/watcher/current/appendix-api-execute-watch.html>`_

        :arg id: Watch ID
        :arg body: Execution control
        """
        if id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'id'.")
        _, data = self.transport.perform_request('PUT', _make_path('_watcher',
            'watch', id, '_execute'), params=params, body=body)
        return data

    @query_params()
    def get_watch(self, id, params=None):
        """
        `<http://www.elastic.co/guide/en/watcher/current/appendix-api-get-watch.html>`_

        :arg id: Watch ID
        """
        if id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'id'.")
        _, data = self.transport.perform_request('GET', _make_path('_watcher',
            'watch', id), params=params)
        return data

    @query_params()
    def delete_watch(self, id, params=None):
        """
        `<http://www.elastic.co/guide/en/watcher/current/appendix-api-delete-watch.html>`_

        :arg id: Watch ID
        """
        if id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'id'.")
        _, data = self.transport.perform_request('DELETE',
            _make_path('_watcher', 'watch', id), params=params)
        return data

    @query_params()
    def restart(self, params=None):
        """
        `<http://www.elastic.co/guide/en/watcher/current/appendix-api-service.html>`_
        """
        _, data = self.transport.perform_request('PUT', '/_watcher/_restart',
            params=params)
        return data

