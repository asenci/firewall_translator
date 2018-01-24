from logging import debug, info


class Rule:
    matches = None
    action = None
    action_params = None

    def __init__(self, matches=None, action=None, action_params=None):
        self.matches = matches
        self.action = action
        self.action_params = action_params


class Chain:
    name = None
    rules = None
    default_action = None

    def __init__(self, name, rules=None, def_action='-'):
        self.name = name

        if rules:
            self.rules = rules
        else:
            self.rules = []

    def append(self, rule):
        self.rules.append(rule)

    def insert(self, rule, position=0):
        self.rules.insert(position, rule)

    def delete(self, rule):
        self.rules.remove(rule)


class Table:
    name = None
    chains = None

    def __init__(self, name, chains=None):
        self.name = name

        if chains:
            self.chains = chains
        else:
            self.chains = {}

    def new_chain(self, name, rules=None, def_action='-'):
        if name in self.chains:
            raise KeyError

        self.chains[name] = Chain(name, rules, def_action)

    def delete_chain(self, name):
        del(self.chains[name])


class RuleSet:
    tables = None

    def __init__(self, tables=None):
        if tables:
            self.tables = tables
        else:
            self.tables = {
                'filter': Table('filter', {
                    'FORWARD': Chain('FORWARD', def_action='ACCEPT'),
                    'INPUT': Chain('INPUT', def_action='ACCEPT'),
                    'OUTPUT': Chain('OUTPUT', def_action='ACCEPT'),
                }),
                'mangle': Table('mangle', {
                    'FORWARD': Chain('FORWARD', def_action='ACCEPT'),
                    'INPUT': Chain('INPUT', def_action='ACCEPT'),
                    'OUTPUT': Chain('OUTPUT', def_action='ACCEPT'),
                    'POSTROUTING': Chain('POSTROUTING', def_action='ACCEPT'),
                    'PREROUTING': Chain('PREROUTING', def_action='ACCEPT'),
                }),
                'nat': Table('nat', {
                    'INPUT': Chain('INPUT', def_action='ACCEPT'),
                    'OUTPUT': Chain('OUTPUT', def_action='ACCEPT'),
                    'POSTROUTING': Chain('POSTROUTING', def_action='ACCEPT'),
                    'PREROUTING': Chain('PREROUTING', def_action='ACCEPT'),
                }),
            }

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
                    self.tables[table].new_chain(name, def_action=action)

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
                    matches, action = rule.split('-j')
                else:
                    matches = rule
                    action = None

                matches = matches.strip().split(' ')
                matches_keys = matches[::2]
                matches_values = matches[1::2]
                matches = dict(zip(matches_keys, matches_values))

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

                rule = Rule(matches, action, action_params)

                info('Table: {}, Chain: {}, Action: {}, Params: {}, Matches: {}'.format(table, chain, action, action_params, matches))
                self.tables[table].chains[chain].append(rule)

    def read_from_file(self, file):
        with open(file) as r:
            self.read(r.read())
