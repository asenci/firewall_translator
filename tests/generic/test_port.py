import pytest

from firewall_translator.generic import Port, Protocol


@pytest.mark.parametrize('p_protocol, p_num, p_name, p_repr, p_str',
                         [
                             (Protocol(1), 8, None, '<Port ip/1/8>', 'ip/1/8'),
                             (Protocol(1), 0, 'echo-request', '<Port ip/1/0(echo-request)>', 'echo-request'),
                             (Protocol(6, 'tcp'), 80, None, '<Port tcp/80>', 'tcp/80'),
                             (Protocol(6, 'tcp'), 443, 'https', '<Port tcp/443(https)>', 'https'),
                         ])
def test_port(p_protocol, p_num, p_name, p_repr, p_str):
    p = Port(p_protocol, p_num, p_name)
    assert p.name == p_name
    assert p.number == p_num
    assert p.protocol == p_protocol
    assert repr(p) == p_repr
    assert str(p) == p_str
