import pytest

from firewall_translator.generic import Protocol


@pytest.mark.parametrize('p_num, p_name, p_repr, p_str',
                         [
                             (1, None, '<Protocol 1>', 'ip/1'),
                             (6, 'tcp', '<Protocol 6(tcp)>', 'tcp'),
                             (17, '', '<Protocol 17>', 'ip/17'),
                         ])
def test_protocol(p_num, p_name, p_repr, p_str):
    p = Protocol(p_num, p_name)
    assert p.name == p_name
    assert p.number == p_num
    assert repr(p) == p_repr
    assert str(p) == p_str
