class DnsRecord:
    def __init__(self, bearer, domain, subdomain, dns_type, data_format):
        self.bearer = bearer
        self.domain = domain
        self.subdomain = subdomain
        self.dns_type = dns_type
        self.data_format = data_format
        self.current_value = None
