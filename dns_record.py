import re


class DnsRecord:
    def __init__(self, bearer, domain, subdomain, dns_type, data_format):
        self.bearer = bearer
        self.domain = domain
        self.subdomain = subdomain
        self.dns_type = dns_type
        self.data_format = data_format
        self.current_value = None

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
