class DnsRecord:
    def __init__(self, bearer, domain, subdomain, type, format):
        self.bearer = bearer
        self.domain = domain
        self.subdomain = subdomain
        self.type = type
        self.format = format
        self.current_value = None
