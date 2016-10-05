from urllib.request import urljoin
import requests

BASE_URL = 'https://api.digitalocean.com/'


def get_domain_records(bearer, domain):
    url = '/v2/domains/{domain}/records'.format(domain=domain)

    response = call('GET', url, bearer)

    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError('Unexpected response ({code}) while getting domain records'.format(code=response.status_code),
                         domain, get_api_response_error_text(response))


def create_domain_record(bearer, domain, data):
    url = '/v2/domains/{domain}/records'.format(domain=domain)

    response = call('POST', url, bearer, data)

    if response.status_code == 201:
        return response.json()
    else:
        raise ValueError('Unexpected response ({code}) while creating domain record'.format(code=response.status_code),
                         domain, get_api_response_error_text(response))


def update_domain_record(bearer, domain, record_id, data):
    url = '/v2/domains/{domain}/records/{id}'.format(domain=domain, id=record_id)

    response = call('PUT', url, bearer, data)

    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError('Unexpected response ({code}) while updating domain record'.format(code=response.status_code),
                         domain, get_api_response_error_text(response))


def call(method, url, bearer, data=None):
    absolute_url = urljoin(BASE_URL, url)
    auth_header = get_auth_header(bearer)

    return requests.request(method, absolute_url, headers=auth_header, data=data)


def get_api_response_error_text(response):
    try:
        json = response.json()

        if 'id' in json and 'message' in json:
            return '{id}: {message}'.format(id=json['id'], message=json['message'])
        else:
            return response.text
    except ValueError:
        return response.text


def get_auth_header(bearer):
    return {'Authorization': 'Bearer {key}'.format(key=bearer)}
