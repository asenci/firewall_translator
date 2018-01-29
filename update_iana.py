import os
import requests
import lxml.etree

PROTOCOLS_URL = 'https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xml'
SERVICES_URL = 'https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xml'
XML_NS = {None: 'http://www.iana.org/assignments'}


def get_xml(url):
    response = requests.get(url)
    response.raise_for_status()
    response.close()

    return lxml.etree.fromstring(response.content, base_url=url)


def get_protocols_from_iana():
    xml = get_xml(PROTOCOLS_URL)
    for registry in xml.iterfind('registry', namespaces=XML_NS):
        for record in registry.iterfind('record', namespaces=XML_NS):
            name = record.findtext('name', namespaces=XML_NS)
            numbers = record.findtext('value', namespaces=XML_NS)

            if name and numbers:
                name = name.partition(' ')[0].lower()

                if '-' in numbers:
                    start, stop = numbers.split('-')
                    start, stop = int(start), (int(stop) + 1)
                    numbers = range(start, stop)
                else:
                    numbers = [int(numbers)]

                for number in numbers:
                    yield name, number


def get_services_from_iana():
    xml = get_xml(SERVICES_URL)
    for record in xml.iterfind('record', namespaces=XML_NS):
        protocol = record.findtext('protocol', namespaces=XML_NS)
        name = record.findtext('name', namespaces=XML_NS)
        numbers = record.findtext('number', namespaces=XML_NS)

        if protocol and name and numbers:
            protocol = protocol.lower()
            name = name.partition(' ')[0].lower()

            if '-' in numbers:
                start, stop = numbers.split('-')
                start, stop = int(start), (int(stop) + 1)
                numbers = range(start, stop)
            else:
                numbers = [int(numbers)]

            for number in numbers:
                yield protocol, name, number


def protocols_gen():
    protocols_list = sorted(get_protocols_from_iana())

    yield 'PROTOCOLS = {'
    for name, number in protocols_list:
        yield '    \'{}\': Protocol({}, \'{}\'),'.format(name, number, name)
    yield '}'


def services_gen():
    services_dict = {}
    for protocol, name, number in get_services_from_iana():
        if protocol not in services_dict:
            services_dict[protocol] = {name: number}
        else:
            services_dict[protocol].update({name: number})

    yield 'SERVICES = {'
    for protocol, services in sorted(services_dict.items()):
        yield '    \'{}\': {{'.format(protocol)
        for name, number in sorted(services.items()):
            yield '        \'{}\': Service(PROTOCOLS[\'{}\'], {}, \'{}\'),'.format(name, protocol, number, name)
        yield '    },'
    yield '}'


def main():
    file_path = os.path.join(os.path.dirname(__file__), 'firewall_translator', 'iana.py')
    with open(file_path, 'w') as f:
        f.write('from firewall_translator.generic import Protocol, Service\n')
        f.write('\n')

        for generator in [protocols_gen, services_gen]:
            for line in generator():
                f.write(line)
                f.write('\n')


if __name__ == '__main__':
    main()
