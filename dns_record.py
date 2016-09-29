from urllib.request import urljoin
import requests
import re


class DnsRecord:
    API_BASE_URL = 'https://api.digitalocean.com/'


    def __init__(self, bearer, domain, subdomain, dns_type, data_format):
        self.bearer = bearer
        self.domain = domain
        self.subdomain = subdomain
        self.dns_type = dns_type
        self.data_format = data_format
        self.current_value = None
        self.id = None

    def refresh(self, ipv4: str, ipv6: str):
        new_value = self.string_replace(self.data_format, ipv4=ipv4, ipv6=ipv6)

        if not new_value == self.current_value:
            self.push(new_value)

    def push(self, value: str):
        self.current_value = value

        if self.id is None:
            self.create_record()
        else:
            self.update_record()

    def create_record(self):
        url = format('/v2/domains/{domain}/records', domain=self.domain)
        absolute_url = urljoin(DnsRecord.API_BASE_URL, url)

        return requests.post(absolute_url, self.get_request_data())

    def update_record(self):
        url = format('/v2/domains/{domain}/records/{id}', domain=self.domain, id=self.id)
        absolute_url = urljoin(DnsRecord.API_BASE_URL, url)

        return requests.put(absolute_url, self.get_request_data())

    def get_request_data(self):
        return {
            'type': self.dns_type,
            'name': self.subdomain,
            'data': self.current_value
        }

    def matches_record(self, record: dict):
        return record['type'] == self.dns_type and \
               record['name'] == self.subdomain and \
               self.value_matches_format(record['data'], self.data_format)

    def set_base_record(self, record: dict):
        self.id = record['id']
        self.current_value = record['data']

    @staticmethod
    def string_replace(string: str, ipv4: str, ipv6: str):
        replacements = [('%v4', ipv4),
                        ('%v6', ipv6),
                        ('%%', '%')]

        result = ''

        while len(string) > 0:
            if not string[0] == '%':
                result += string[0]
                string = string[1:]

            else:
                for key, value in replacements:
                    if string.startswith(key):
                        result += value
                        string = string[len(key):]

        return result

    @staticmethod
    def generate_format(string: str, replace_literals=True):
        if replace_literals:
            replacements = [(r'%', '%%')]
        else:
            replacements = []

        replacements += [(r"(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)", '%v4'),
                         (r"(?:[A-F0-9]{1,4}:){7}[A-F0-9]{1,4}", '%v6')]

        for regex, token in replacements:
            string = re.sub(regex, token, string)

        return string

    # WARNING: False positives.
    # Example: "1.2.3.4, 5.6.7.8" matches "%v4 %v4"
    @staticmethod
    def value_matches_format(value: str, data_format: str):
        return DnsRecord.generate_format(data_format, replace_literals=False) == DnsRecord.generate_format(value)
