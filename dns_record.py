import re
import api


class DnsRecord:
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
            api.create_domain_record(self.bearer, self.domain, self.get_request_data())
        else:
            api.update_domain_record(self.bearer, self.domain, self.id, self.get_request_data())

    def get_request_data(self):
        return {
            'type': self.dns_type,
            'name': self.subdomain,
            'data': self.current_value
        }

    def matches_record(self, record: dict):
        type_matches = record['type'] == self.dns_type
        subdomain_matches = record['name'] == self.subdomain
        format_matches = self.value_matches_format(record['data'], self.data_format)

        if self.dns_type in ['A', 'AAAA']:
            return type_matches and subdomain_matches
        else:
            return type_matches and subdomain_matches and format_matches

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
            string = re.sub(regex, token, string, flags=re.IGNORECASE)

        return string

    @staticmethod
    def value_matches_format(value: str, data_format: str):
        return DnsRecord.generate_format(data_format, replace_literals=False) == DnsRecord.generate_format(value)


class DnsRecordFactory:
    def __init__(self):
        self.bearer = None
        self.domain = None
        self.records = []

    def get_all_records(self):
        return self.records

    def set_bearer(self, bearer):
        self.bearer = bearer

    def set_domain(self, domain):
        self.domain = domain

    def create_records(self, subdomain, dns_type=None, data_format=None):
        if data_format is not None:
            if dns_type is not None:
                self.records.append(DnsRecord(self.bearer, self.domain, subdomain, dns_type, data_format))
            else:
                self.create_records(subdomain, dns_type='TXT', data_format=data_format)
        else:
            if dns_type is None:
                self.create_records(subdomain, dns_type='A')
                self.create_records(subdomain, dns_type='AAAA')
            elif dns_type == 'A':
                self.create_records(subdomain, dns_type=dns_type, data_format='%v4')
            elif dns_type == 'AAAA':
                self.create_records(subdomain, dns_type=dns_type, data_format='%v6')
            else:
                raise Exception('Format must be set for type ' + dns_type)