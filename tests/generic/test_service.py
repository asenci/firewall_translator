import pytest

from firewall_translator.generic import Service, Protocol


@pytest.mark.parametrize('p_protocol, p_num, p_name, p_repr, p_str',
                         [
                             (Protocol(1), 8, None, '<Service ip/1/8>', 'ip/1/8'),
                             (Protocol(1), 0, 'echo-request', '<Service ip/1/0(echo-request)>', 'echo-request'),
                             (Protocol(6, 'tcp'), 80, None, '<Service tcp/80>', 'tcp/80'),
                             (Protocol(6, 'tcp'), 443, 'https', '<Service tcp/443(https)>', 'https'),
                         ])
def test_service(p_protocol, p_num, p_name, p_repr, p_str):
    p = Service(p_protocol, p_num, p_name)
    assert p.name == p_name
    assert p.number == p_num
    assert p.protocol == p_protocol
    assert repr(p) == p_repr
    assert str(p) == p_str
