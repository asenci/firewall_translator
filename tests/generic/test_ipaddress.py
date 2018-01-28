import pytest

from firewall_translator.generic import IPAddress


@pytest.mark.parametrize('ip_addr, ip_name, ip_addr_str, ip_repr, ip_str',
                         [
                             ('127.0.0.1', 'localhost', '127.0.0.1/32', '<IPAddress 127.0.0.1/32(localhost)>', 'localhost'),
                             ('127.0.0.1/8', None, '127.0.0.0/8', '<IPAddress 127.0.0.0/8>', '127.0.0.0/8'),
                             ('192.168.0.0/24', 'lan', '192.168.0.0/24', '<IPAddress 192.168.0.0/24(lan)>', 'lan'),
                         ])
def test_ip_address(ip_addr, ip_name, ip_addr_str, ip_repr, ip_str):
    ip = IPAddress(ip_addr, ip_name)
    assert ip.name == ip_name
    assert str(ip.address) == ip_addr_str
    assert repr(ip) == ip_repr
    assert str(ip) == ip_str
