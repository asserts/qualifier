import json
import requests
from requests.exceptions import RequestException, HTTPError


class QueryClient:
    """QueryClient for making http requests"""

    def __init__(self, host):
        """
        Args:
            host (str): The host to make queries against

        Attrs:
            host (str): The host to make queries against
            headers (dict): http headers
        """

        self.host = host
        self.headers = {}

    def set_header(self, key, val):
        """Set an http header for this QueryClient

        Args:
            key (str): header key
            val (str): header val
        """

        self.headers[key] = val

    def _run_instant_query(self, query, request_type, limit=None, data=None):
        """Handle http requests for the QueryClient

        Args:
            query (str): the query to run
            request_type (str): the request type (valid types = ['GET', 'POST'])
            limit (int): the limit to use, implies wrapping query in "topk(limit, query)"
            data (dict): the data to POST (default=None)

        Returns:
            dict: the json response
        """

        json_response = {}
        instant_query = '/api/v1/query'

        if limit:
            query = f'topk({limit}, {query})'

        url = self.host + instant_query
        try:
            print(f'Performing method={request_type} for client={self.__class__.__name__} at url={url} with query={query}')

            if request_type == 'GET':
                self.set_header('Content-Type', 'application/json')
                r = requests.get(url, params={'query': query}, headers=self.headers)
            elif request_type == 'POST':
                self.set_header('Content-Type', 'application/json')
                r = requests.post(url, params={'query': query}, headers=self.headers, data=data)
        except RequestException as e:
            raise(e)
        except HTTPError as e:
            raise(e)

        if r.status_code == 200:
            json_response = json.loads(r.text)
        else:
            msg = f'{request_type} request to url={url} received status_code={r.status_code}.\n{r.text}'
            print(msg)
            json_response = None

        return json_response

    def instant_query(self, query, request_type='GET', limit=None, data=None):
        """Run an instant query against the QueryClient's host

        Args:
            query (str): the query to run
            request_type (str): the request type (valid types = ['GET', 'POST'])
            limit (int): the limit to use, implies wrapping query in "topk(limit, query)"
            data (dict): the data to POST (default=None)

        Returns:
            dict: the json response
        """

        response = self._run_instant_query(query, request_type, limit, data)
        result = response['data']['result']
        if not result:
            print('Result empty\n')

        return result