import pytest

from firewall_translator.generic import Action


@pytest.mark.parametrize('a_allow, a_reply, a_log, a_repr, a_str',
                         [
                             (False, False, False, '<Action deny>', 'deny'),
                             (False, False, True, '<Action deny log>', 'deny and log'),
                             (False, True, False, '<Action deny reply>', 'deny with ICMP reply'),
                             (False, True, True, '<Action deny reply log>', 'deny with ICMP reply and log'),
                             (True, False, False, '<Action allow>', 'allow'),
                             (True, False, True, '<Action allow log>', 'allow and log'),
                             (True, True, False, 'NotImplemented', 'NotImplementedError'),
                             (True, True, True, 'NotImplemented', 'NotImplementedError'),
                         ])
def test_action_allow(a_allow, a_reply, a_log, a_repr, a_str):
    if a_allow and a_reply:
        with pytest.raises(NotImplementedError):
            a = Action(a_allow, a_reply, a_log)

    else:
        a = Action(a_allow, a_reply, a_log)
        assert a.allow is a_allow
        assert a.reply is a_reply
        assert a.log is a_log
        assert repr(a) == a_repr
        assert str(a) == a_str
