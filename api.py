from urllib.request import urljoin
import requests

BASE_URL = 'https://api.digitalocean.com/'


def get_domain_records(bearer, domain):
    url = '/v2/domains/{domain}/records'.format(domain=domain)

    response = call('GET', url, bearer)
    return response.json()


def create_domain_record(bearer, domain, data):
    url = '/v2/domains/{domain}/records'.format(domain=domain)

    response = call('POST', url, bearer, data)
    return response.json()


def update_domain_record(bearer, domain, record_id, data):
    url = '/v2/domains/{domain}/records/{id}'.format(domain=domain, id=record_id)

    response = call('PUT', url, bearer, data)
    return response.json()


def call(method, url, bearer, data=None):
    absolute_url = urljoin(BASE_URL, url)
    auth_header = get_auth_header(bearer)

    return requests.request(method, absolute_url, headers=auth_header, data=data)


def get_auth_header(bearer):
    return {'Authorization': 'Bearer {key}'.format(key=bearer)}
