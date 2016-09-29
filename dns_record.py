import re


class DnsRecord:
    def __init__(self, bearer, domain, subdomain, dns_type, data_format):
        self.bearer = bearer
        self.domain = domain
        self.subdomain = subdomain
        self.dns_type = dns_type
        self.data_format = data_format
        self.current_value = None
        self.id = None

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
