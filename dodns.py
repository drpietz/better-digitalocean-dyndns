import json
import requests
import socket
from dns_record import DnsRecordFactory
import api
import os
from configparser import ConfigParser


def main():
    hostname = get_hostname()

    records = get_records_from_config(hostname)
    fetch_current_data(records)
    update_records(records)


def update_records(records):
    ipv4 = get_current_ipv4_address()
    ipv6 = get_current_ipv6_address()

    for record in records:
        record.refresh(ipv4, ipv6)


def fetch_current_data(records):
    domain_records = {}

    for record in records:
        if record.domain not in domain_records:
            domain_records[record.domain] = api.get_domain_records(record.bearer, record.domain)['domain_records']

        current_domain_records = domain_records[record.domain]

        for domain_record in current_domain_records:
            if record.matches_record(domain_record):
                record.set_base_record(domain_record)

                current_domain_records.remove(domain_record)
                break


def get_records_from_config(hostname):
    factory = DnsRecordFactory()

    with open(get_relative_file('config.json')) as json_data:
        config = json.load(json_data)

    for bearer in config['bearers']:
        factory.set_bearer(bearer['key'])

        for domain in bearer['domains']:
            factory.set_domain(domain['name'])

            for record in domain['dyn_records']:
                if 'host' not in record or record['host'] == hostname:
                    factory.create_records(record['name'], record.get('type'), record.get('data'))

    return factory.get_all_records()


def get_hostname():
    return get_config_value('Hostname', socket.gethostname())


def get_config_value(name, default=None):
    if not os.path.isfile(get_relative_file('config.ini')):
        return default

    config = ConfigParser()
    config.read('config.ini')

    if 'Dodns' in config and name in config['Dodns']:
        return config['Dodns'][name]
    else:
        return default


def get_relative_file(file):
    return os.path.join(os.path.dirname(__file__), file)


def get_current_ipv4_address():
    ipv4 = get_page_content('http://ipv4bot.whatismyipaddress.com/')
    if is_valid_ipv4_address(ipv4):
        return ipv4
    else:
        raise ValueError('Returned value is not a valid IPv4 address', ipv4)


def get_current_ipv6_address():
    ipv6 = get_page_content('http://ipv6bot.whatismyipaddress.com/')
    if is_valid_ipv6_address(ipv6):
        return ipv6
    else:
        raise ValueError('Returned value is not a valid IPv6 address', ipv6)


def get_page_content(url):
    return requests.get(url).text


def is_valid_ipv4_address(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:  # not a valid address
        return False

    return True


def is_valid_ipv6_address(address):
    try:
        socket.inet_pton(socket.AF_INET6, address)
    except socket.error:  # not a valid address
        return False
    return True


if __name__ == '__main__':
    main()
