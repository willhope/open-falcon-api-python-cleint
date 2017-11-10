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
            self._session.headers = {
                'Content-Type': 'application/json; charset=utf-8',
                'Accept': 'application/json',
                'Apitoken': json.dumps(api_token),
                "X-Forwarded-For": "127.0.0.1"
            }

    def __getattr__(self, key):
        if key in self.__dict__:
            return self.__dict__[key]

        return self.__class__(
            endpoint=self._endpoint,
            keys=self._keys + [key],
            session=self._session)

    def __getitem__(self, key):
        return self.__getattr__(key)

    def __call__(self, **kwargs):
        method = self._keys[-1]
        url = "/".join(self._keys[0:-1])
        url = url.strip("/")
        return self.do_request(method, url, **kwargs)

    def do_request(self, method, url, params=None):
        url = self._endpoint + self._url_prex + url

        if not params:
            params = {}

        if method == 'get' or method == 'list':
            url = url + '?' + urlencode(params, doseq=True)
            response = self._session.get(url, verify=self.ssl_verify)

        if method == 'post'or method == 'create':
            url = url + '?' + urlencode(params, doseq=True)
            response = self._session.post(url, verify=self.ssl_verify)

        if method == 'put'or method == 'update':
            response = self._session.put(url, data=json.dumps(params), verify=self.ssl_verify)

        if method == 'delete':
			url = url + '?' + urlencode(params, doseq=True)
            response = self._session.delete(url, verify=self.ssl_verify)

        try:
            body = json.loads(response.text)
        except ValueError:
            body = "Get unknow error from falcon:%s" % response.text
        if response.status_code >= 400:
            message = body
            raise exceptions.from_response(response.status_code, self.url, method, message)

        return body

