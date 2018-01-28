import ipaddress


class Action:
    allow = False
    log = False
    reply = False

    def __init__(self, allow=False, reply=False, log=False):
        if allow and reply:
            raise NotImplementedError('ICMP reply not allowed when allowing traffic')

        self.allow = allow
        self.reply = reply
        self.log = log

    def __repr__(self):
        actions = []

        if self.allow:
            actions.append('allow')
        else:
            actions.append('deny')

        if self.reply:
            actions.append('reply')

        if self.log:
            actions.append('log')

        return '<{} {}>'.format(self.__class__.__name__, ' '.join(actions))

    def __str__(self):
        actions = []

        if self.allow:
            actions.append('allow')
        else:
            actions.append('deny')

        if self.reply:
            actions.append('with ICMP reply')

        if self.log:
            actions.append('and log')

        return ' '.join(actions)


class Interface:
    name = None

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.name)

    def __str__(self):
        return self.name


class IPAddress:
    address = None
    name = None

    def __init__(self, address, name=None):
        self.address = ipaddress.ip_interface(address).network

        if name is not None:
            self.name = name

    def __repr__(self):
        if self.name:
            return '<{} {}({})>'.format(self.__class__.__name__, self.address, self.name)

        return '<{} {}>'.format(self.__class__.__name__, self.address)

    def __str__(self):
        if self.name:
            return self.name

        return str(self.address)


class NAT:
    pass


class Port:
    name = None
    number = None
    protocol = None

    def __init__(self, protocol, number, name=None):
        self.protocol = protocol
        self.number = number

        if name is not None:
            self.name = name

    def __repr__(self):
        if self.name:
            return '<{} {}/{}({})>'.format(self.__class__.__name__, self.protocol, self.number, self.name)

        return '<{} {}/{}>'.format(self.__class__.__name__, self.protocol, self.number)

    def __str__(self):
        if self.name:
            return self.name

        return '{}/{}'.format(self.protocol, self.number)


class Protocol:
    name = None
    number = None

    def __init__(self, number, name=None):
        self.number = number

        if name is not None:
            self.name = name

    def __repr__(self):
        if self.name:
            return '<{} {}({})>'.format(self.__class__.__name__, self.number, self.name)

        return '<{} {}>'.format(self.__class__.__name__, self.number)

    def __str__(self):
        if self.name:
            return self.name

        return 'ip/{}'.format(str(self.number))


class Rule:
    pass


class TimeRange:
    def __init__(self):
        raise NotImplementedError('Time range must be either absolute or periodic')


class AbsoluteTimeRange(TimeRange):
    start = None
    stop = None

    # noinspection PyMissingConstructor
    def __init__(self, start, stop):
        if start > stop:
            raise RuntimeError('Stop date before start date')
        self.start = start
        self.stop = stop

    def __repr__(self):
        return '<{} {:%Y-%m-%dT%H:%M} {:%Y-%m-%dT%H:%M}>'.format(self.__class__.__name__, self.start, self.stop)

    def __str__(self):
        return 'from {:%Y-%m-%d %H:%M} to {:%Y-%m-%d %H:%M}'.format(self.start, self.stop)


class PeriodicTimeRange(TimeRange):
    start = None
    stop = None
    weekdays = None

    # noinspection PyMissingConstructor
    def __init__(self, start, stop,
                 sunday=True, monday=True, tuesday=True,
                 wednesday=True, thursday=True, friday=True, saturday=True):
        if start > stop:
            raise RuntimeError('Stop time before start time')

        weekdays = [sunday, monday, tuesday, wednesday, thursday, friday, saturday]
        if not any(weekdays):
            raise RuntimeError('No day of the week selected')

        self.start = start
        self.stop = stop
        self.weekdays = weekdays

    def __repr__(self):
        return '<{} {:%H:%M} {:%H:%M} {}>'.format(self.__class__.__name__, self.start, self.stop, self.weekdays)

    def __str__(self):
        if all(self.weekdays):
            return 'daily from {:%H:%M} to {:%H:%M}'.format(self.start, self.stop)

        days = []

        if self.weekdays[0]:
            days.append('sun')
        if self.weekdays[1]:
            days.append('mon')
        if self.weekdays[2]:
            days.append('tue')
        if self.weekdays[3]:
            days.append('wed')
        if self.weekdays[4]:
            days.append('thu')
        if self.weekdays[5]:
            days.append('fri')
        if self.weekdays[6]:
            days.append('sat')

        return 'from {:%H:%M} to {:%H:%M} on {}'.format(self.start, self.stop, ', '.join(days))
