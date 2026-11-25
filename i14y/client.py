import json
import os

import requests
import urllib3

from . import config


def already_has_i14y_state(response, field, value):
    """Recognize only an explicit already-at-target 405, including forwarded errors."""
    if response.status_code != 405:
        return False
    try:
        problem = json.loads(response.text)
        detail = problem.get('detail', '')
        if 'Response:' in detail:
            forwarded = json.loads(detail.split('Response:', 1)[1].strip())
            detail = forwarded.get('detail', '')
        return detail == f"The resource already has its {field} set to '{value}'."
    except (ValueError, TypeError, AttributeError):
        return False


class I14YClient:
    def __init__(self):
        self.token = os.environ['ACCESS_TOKEN']
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.token}',
            'Accept': 'application/json',
        })
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def request(self, method, path, **kwargs):
        response = self.session.request(
            method, config.API_BASE_URL + path, verify=False, timeout=40.0, **kwargs
        )
        self.raise_for_status(response)
        return response

    def raise_for_status(self, response):
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            detail = response.text
            if self.token:
                detail = detail.replace(self.token, '[REDACTED]')
            raise requests.exceptions.HTTPError(
                f"{error}\nI14Y-Antwort: {detail}", response=response
            ) from error

    def find(self, endpoint, identifier_parameter, identifier):
        response = self.request(
            'GET', endpoint,
            params={identifier_parameter: identifier, 'page': 1, 'pageSize': 25},
        )
        matches = response.json()['data']
        if len(matches) > 1:
            raise ValueError(f"Mehrere I14Y-Einträge unter {endpoint} für {identifier}.")
        return matches[0] if matches else None

    def set_state(self, path, parameter, value, field):
        response = self.session.put(
            config.API_BASE_URL + path, params={parameter: value},
            verify=False, timeout=40.0,
        )
        if already_has_i14y_state(response, field, value):
            print(f"I14Y: {field} ist bereits {value}.")
            return
        self.raise_for_status(response)
