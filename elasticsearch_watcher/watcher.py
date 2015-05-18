from elasticsearch.client.utils import AddonClient, query_params, _make_path, SKIP_IN_PATH

class WatcherClient(AddonClient):
    namespace = 'watcher'
    @query_params()
    def info(self, params=None):
        """
        Get infor about the watcher plugin.
        `<http://www.elastic.co/guide/en/watcher/current/appendix-api-info.html>`_
        """
        _, data = self.transport.perform_request('GET', '/_watcher/',
            params=params)
        return data

    @query_params('master_timeout')
    def put_watch(self, id, body, params=None):
        """
        Create a watcher.
        `<http://www.elastic.co/guide/en/watcher/current/appendix-api-put-watch.html>`_

        :arg id: Watch ID
        :arg body: The watch
        :arg master_timeout: Specify timeout for watch write operation
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
        Get stats for the watcher plugin.
        `<http://www.elastic.co/guide/en/watcher/current/appendix-api-stats.html>`_
        """
        _, data = self.transport.perform_request('GET', '/_watcher/stats',
            params=params)
        return data

    @query_params()
    def stop(self, params=None):
        """
        Stop the watcher service.
        `<http://www.elastic.co/guide/en/watcher/current/appendix-api-service.html>`_
        """
        _, data = self.transport.perform_request('PUT', '/_watcher/_stop',
            params=params)
        return data

    @query_params()
    def start(self, params=None):
        """
        Start the watcher service.
        `<http://www.elastic.co/guide/en/watcher/current/appendix-api-service.html>`_
        """
        _, data = self.transport.perform_request('PUT', '/_watcher/_start',
            params=params)
        return data

    @query_params('master_timeout')
    def ack_watch(self, id, params=None):
        """
        Ack a watch.
        `<http://www.elastic.co/guide/en/watcher/current/appendix-api-ack-watch.html>`_

        :arg id: Watch ID
        :arg master_timeout: Specify timeout for watch write operation
        """
        if id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'id'.")
        _, data = self.transport.perform_request('PUT', _make_path('_watcher',
            'watch', id, '_ack'), params=params)
        return data

    @query_params()
    def execute_watch(self, id, body=None, params=None):
        """
        Execute watch manually.
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
        Retrieve watch definition.
        `<http://www.elastic.co/guide/en/watcher/current/appendix-api-get-watch.html>`_

        :arg id: Watch ID
        """
        if id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'id'.")
        _, data = self.transport.perform_request('GET', _make_path('_watcher',
            'watch', id), params=params)
        return data

    @query_params('force', 'master_timeout')
    def delete_watch(self, id, params=None):
        """
        Delete a watch.
        `<http://www.elastic.co/guide/en/watcher/current/appendix-api-delete-watch.html>`_

        :arg id: Watch ID
        :arg force: Specify if this request should be forced and ignore locks
        :arg master_timeout: Specify timeout for watch write operation
        """
        if id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'id'.")
        _, data = self.transport.perform_request('DELETE',
            _make_path('_watcher', 'watch', id), params=params)
        return data

    @query_params()
    def restart(self, params=None):
        """
        Restart the watcher service.
        `<http://www.elastic.co/guide/en/watcher/current/appendix-api-service.html>`_
        """
        _, data = self.transport.perform_request('PUT', '/_watcher/_restart',
            params=params)
        return data

