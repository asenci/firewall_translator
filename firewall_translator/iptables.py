import collections
import logging

import firewall_translator.generic


class Action(firewall_translator.generic.Action):
    def __init__(self, allow=False, reply=False, log=False):
        if log:
            raise NotImplementedError
        super(Action, self).__init__(allow, reply, log)

    def __repr__(self):
        pass

    def __str__(self):
        if self.allow:
            return 'ACCEPT'

        elif self.reply:
            return 'REJECT'

        return 'DROP'


class Rule:
    match_params = None
    action = None
    action_params = None

    def __init__(self, match_params=None, action=None, action_params=None):
        self.match_params = match_params
        self.action = action
        self.action_params = action_params

    def __repr__(self):
        string = '<{}'.format(self.__class__.__name__)

        if self.match_params:
            string += ' Match: {!r}'.format(self.match_params)

        if self.action:
            string += ' Action: {}'.format(self.action)

        if self.action_params:
            string += ' {!r}'.format(self.action_params)

        string += '>'
        return string

    def __str__(self):
        string = []

        if self.match_params:
            for k, v in self.match_params.items():
                string.append(' '.join([k, v]))

        if self.action:
            string.append('-j {}'.format(self.action))

        if self.action_params:
            for k, v in self.action_params.items():
                string.append(' '.join([k, v]))

        return ' '.join(string)

    @staticmethod
    def from_cli(string):
        match_params, action = string.partition(' -j ')[::2]

        match_params = match_params.strip().split(' ')
        match_params_keys = match_params[::2]
        match_params_values = match_params[1::2]
        match_params = dict(zip(match_params_keys, match_params_values))

        action_params = None

        if action:
            action = action.strip()
            if ' ' in action:
                info(action)
                action, action_params = action.split(' ', 1)

        if action_params:
            action_params = action_params.strip().split(' ')
            action_params_keys = action_params[::2]
            action_params_values = action_params[1::2]
            action_params = dict(zip(action_params_keys, action_params_values))

        rule = Rule(match_params, action, action_params)

        info('Table: {}, Chain: {}, Action: {}, Params: {}, Matches: {}'.format(table, chain, action, action_params,
                                                                                match_params))
        self.tables[table].chains[chain].append(rule)


class Chain(collections.MutableSequence, collections.Iterable):
    name = None
    rules = None
    action = None

    def __delitem__(self, index):
        del(self.rules[index])

    def __getitem__(self, index):
        return self.rules[index]

    def __init__(self, name, rules=None, action='-'):
        self.name = name
        self.action = action

        if rules is None:
            self.rules = []
        else:
            self.rules = rules

    def __iter__(self):
        for rule in self.rules:
            yield rule

    def __len__(self):
        return len(self.rules)

    def __repr__(self):
        return '<{} {} {}>'.format(self.__class__.__name__, self.name, self.action)

    def __setitem__(self, index, value):
        self.rules[index] = value

    def __str__(self):
        string = [':{} {} [0:0]'.format(self.name, self.action)]

        for rule in self.rules:
            string.append('-A {} {}'.format(self.name, rule))

        return '\n'.join(string)

    def append(self, rule):
        self.rules.append(rule)

    def insert(self, rule, position=0):
        self.rules.insert(position, rule)

    def delete(self, rule):
        self.rules.remove(rule)


class Table(collections.MutableMapping):
    name = None
    chains = None

    def __delitem__(self, key):
        del(self.chains[key])

    def __getitem__(self, key):
        return self.chains[key]

    def __init__(self, name, chains=None):
        self.name = name

        if chains is None:
            self.chains = {}
        else:
            self.chains = chains

    def __iter__(self):
        for chain in self.chains.values():
            yield chain

    def __len__(self):
        return len(self.chains)

    def __repr__(self):
        return '<{} {} {}>'.format(self.__class__.__name__, self.name, list(self.chains))

    def __setitem__(self, key, value):
        self.chains[key] = value

    def __str__(self):
        string = ['*{}'.format(self.name)]

        for chain in self.chains.values():
            string.append(str(chain))

        string.append('COMMIT')

        return '\n'.join(string)

    def new_chain(self, name, rules=None, action='-'):
        if name in self.chains:
            raise KeyError

        self.chains[name] = Chain(name, rules, action)

    def delete_chain(self, name):
        del(self.chains[name])


class RuleSet(collections.MutableMapping):
    tables = None

    def __delitem__(self, key):
        del(self.tables[key])

    def __getitem__(self, key):
        return self.tables[key]

    def __init__(self, tables=None):
        if tables is None:
            self.tables = {
                'filter': Table('filter', {
                    'FORWARD': Chain('FORWARD', action='ACCEPT'),
                    'INPUT': Chain('INPUT', action='ACCEPT'),
                    'OUTPUT': Chain('OUTPUT', action='ACCEPT'),
                }),
                'mangle': Table('mangle', {
                    'FORWARD': Chain('FORWARD', action='ACCEPT'),
                    'INPUT': Chain('INPUT', action='ACCEPT'),
                    'OUTPUT': Chain('OUTPUT', action='ACCEPT'),
                    'POSTROUTING': Chain('POSTROUTING', action='ACCEPT'),
                    'PREROUTING': Chain('PREROUTING', action='ACCEPT'),
                }),
                'nat': Table('nat', {
                    'INPUT': Chain('INPUT', action='ACCEPT'),
                    'OUTPUT': Chain('OUTPUT', action='ACCEPT'),
                    'POSTROUTING': Chain('POSTROUTING', action='ACCEPT'),
                    'PREROUTING': Chain('PREROUTING', action='ACCEPT'),
                }),
            }
        else:
            self.tables = tables

    def __iter__(self):
        for table in self.tables.values():
            yield table

    def __len__(self):
        return len(self.tables)

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, list(self.tables))

    def __setitem__(self, key, value):
        self.tables[key] = value

    def __str__(self):
        string = []

        for table in self.tables.values():
            string.append(str(table))

        return '\n'.join(string)

    def read(self, rule_def):
        table = None

        for line in rule_def.splitlines():
            if not line:
                continue

            if line.strip().startswith('#'):
                debug('Found a comment: {}'.format(line))
                continue

            elif line.strip().startswith('*'):
                debug('Found a table definition: {}'.format(line))

                table = line[1:]
                info('Table: {}'.format(table))

                if table not in self.tables.keys():
                    raise KeyError

            elif line.strip().startswith(':'):
                debug('Found a chain definition: {}'.format(line))

                name, action, counters = line[1:].split(' ')
                info('Table: {}, Chain: {}'.format(table, name))

                if name not in self.tables[table].chains.keys():
                    self.tables[table].new_chain(name, action=action)

            elif line.strip() == 'COMMIT':
                debug('Finished reading table {}'.format(table))
                table = None

            else:
                debug('Found a rule definition: {}'.format(line))
                operation, rule = line.split(' ', 1)
                if operation != '-A':
                    raise RuntimeError

                chain, rule = rule.split(' ', 1)

                if '-j' in rule:
                    match_params, action = rule.split('-j')
                else:
                    match_params = rule
                    action = None

                match_params = match_params.strip().split(' ')
                match_params_keys = match_params[::2]
                match_params_values = match_params[1::2]
                match_params = dict(zip(match_params_keys, match_params_values))

                action_params = None

                if action:
                    action = action.strip()
                    if ' ' in action:
                        info(action)
                        action, action_params = action.split(' ', 1)

                if action_params:
                    action_params = action_params.strip().split(' ')
                    action_params_keys = action_params[::2]
                    action_params_values = action_params[1::2]
                    action_params = dict(zip(action_params_keys, action_params_values))

                rule = Rule(match_params, action, action_params)

                info('Table: {}, Chain: {}, Action: {}, Params: {}, Matches: {}'.format(table, chain, action, action_params, match_params))
                self.tables[table].chains[chain].append(rule)

    def read_from_file(self, file):
        with open(file) as r:
            self.read(r.read())
