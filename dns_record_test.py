import unittest
from dns_record import DnsRecord


V4_1 = "162.10.66.0"
V4_2 = "132.145.2.255"
V6_1 = "2001:0db8:0a0b:12f0:0000:0000:0000:0001"


def get_test_record():
    return DnsRecord('b7d03a6947b217efb6f3ec3bd3504582',
                     'example.com',
                     'www',
                     'A',
                     '%v4')


def get_matching_api_record():
    return {
        "id": 3352896,
        "type": "A",
        "name": "www",
        "data": V4_1,
        "priority": None,
        "port": None,
        "weight": None
    }


def get_different_api_record():
    return {
        "id": 3352896,
        "type": "AAAA",
        "name": "www",
        "data": V6_1,
        "priority": None,
        "port": None,
        "weight": None
    }


class TestRecordJoning(unittest.TestCase):
    def setUp(self):
        self.record = get_test_record()
        self.api_record = get_matching_api_record()
        self.different_api_record = get_different_api_record()

    def test_matches_record(self):
        self.assertTrue(self.record.matches_record(self.api_record))
        self.assertFalse(self.record.matches_record(self.different_api_record))

    def test_set_base_record(self):
        self.record.set_base_record(self.api_record)
        self.assertEqual(self.record.id, self.api_record['id'])


class TestFormat(unittest.TestCase):
    def test_string_replace(self):
        self.assertEqual(DnsRecord.string_replace('%v4', ipv4=V4_1, ipv6=V6_1), V4_1)
        self.assertEqual(DnsRecord.string_replace('%v6', ipv4=V4_1, ipv6=V6_1), V6_1)
        self.assertEqual(DnsRecord.string_replace('%%This i%v4s an example %%%v6', ipv4=V4_1, ipv6=V6_1), '%This i' + V4_1 + 's an example %' + V6_1)

    def test_value_format_matching(self):
        self.assertTrue(DnsRecord.value_matches_format(V4_1, '%v4'))
        self.assertTrue(DnsRecord.value_matches_format(V6_1, '%v6'))
        self.assertFalse(DnsRecord.value_matches_format(V4_1, '%v6'))
        self.assertFalse(DnsRecord.value_matches_format(V6_1, '%v4'))
        self.assertTrue(DnsRecord.value_matches_format(V4_1 + ' ' + V6_1, '%v4 %v6'))
        self.assertTrue(DnsRecord.value_matches_format('%' + V4_1 + V4_1 + ' ' + V6_1 + '%', '%%%v4%v4 %v6%%'))
        self.assertTrue(DnsRecord.value_matches_format(V4_1 + '%%', '%v4%%%%'))

    def test_contextual_value_format_matching(self):
        self.assertFalse(DnsRecord.value_matches_format(V4_1 + ' ' + V4_2, '%v4 %v4'))


if __name__ == '__main__':
    unittest.main()
