import pytest

from firewall_translator.generic import Interface


@pytest.mark.parametrize('i_name, i_repr, i_str',
                         [
                             ('lan', '<Interface lan>', 'lan'),
                         ])
def test_interface(i_name, i_repr, i_str):
    i = Interface(i_name)
    assert i.name == i_name
    assert repr(i) == i_repr
    assert str(i) == i_str
