import requests
import json

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
from openfalconclient import exceptions


class FalconClient(object):
    _endpoint = "http://127.0.0.1:8080"
    _url_prex = '/api/v1/'
    _session = None
    _keys = []

    def __init__(self, endpoint=None, user=None, password=None, keys=[], session=None, ssl_verify=True):

        self._keys = keys
        self._session = session
        self.ssl_verify = ssl_verify

        if endpoint:
            self._endpoint = endpoint

        if not session:
            params = {
                "name": user,
                "password": password
            }
            self._session = requests.Session()
            ret = self.do_request('post', 'user/login', params=params)
            api_token = {
                "name": user,
                "sig": ret.get("sig")
            }
            self._session.headers.update({
                'Content-Type': 'application/json; charset=utf-8',
                'Accept': 'application/json',
                'Apitoken': json.dumps(api_token)
            })

    def __getattr__(self, key):
        if key in self.__dict__:
            return self.__dict__[key]

        return self.__class__(
            endpoint=self._endpoint,
            keys=self._keys + [key],
            session=self._session,
            ssl_verify=self.ssl_verify)

    def __getitem__(self, key):
        return self.__getattr__(key)

    def __call__(self, **kwargs):
        method = self._keys[-1]
        url = "/".join(self._keys[0:-1])
        url = url.strip("/")
        return self.do_request(method, url, **kwargs)

    def do_request(self, method, url, params=None, data=None):
        url = self._endpoint + self._url_prex + url

        if params is None:
            params = {}

        if method == 'get' or method == 'list':
            response = self._session.get(url, params=params, verify=self.ssl_verify)

        if method == 'post'or method == 'create':
            response = self._session.post(url, params=params, json=data, verify=self.ssl_verify)

        if method == 'put'or method == 'update':
            response = self._session.put(url, json=data, verify=self.ssl_verify)

        if method == 'delete':
            response = self._session.delete(url, params=params, json=data, verify=self.ssl_verify)

        try:
            body = json.loads(response.text)
        except ValueError:
            body = "Get unknow error from falcon:%s" % response.text
        if response.status_code >= 400:
            message = body
            raise exceptions.from_response(response.status_code, self.url, method, message)

        return body

