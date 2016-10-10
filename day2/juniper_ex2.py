#!/usr/bin/env python
"""Juniper PYEZ config operations."""
from getpass import getpass
from pprint import pprint
from jinja2 import Template

from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.op.routes import RouteTable

# XML Templates
XML_TEMPLATE = """
<configuration>
            <routing-options>
                <static>
                    <route>
                        <name>{{ prefix }}</name>
                        <next-hop>{{ next_hop }}</next-hop>
                    </route>
                </static>
            </routing-options>
</configuration>
"""

def display_static_routes(a_device):
    """Display static routes."""
    routes = RouteTable(a_device)
    routes.get()

    print "\nCurrent static routes"
    print '-' * 50
    pprint(routes.keys())
    print

def generate_route_template(route_dict):
    """Use jinja2 template to construct XML for routes."""
    xml_route = Template(XML_TEMPLATE)
    return str(xml_route.render(**route_dict))

def main():
    """Juniper PYEZ config operations."""
    password = getpass()

    my_route = {
        'prefix': '1.1.2.0/24',
        'next_hop': '10.220.88.1'
    }
    new_route_xml = generate_route_template(my_route)

    # Establish NETCONF connection
    a_device = Device(host='184.105.247.76', user='pyclass', password=password)
    print
    print a_device.open()

    # Create config object
    cfg = Config(a_device)
    cfg.lock()

    # Configure XML
    print "Configuring static routes using XML... (merge)"
    cfg.load(new_route_xml, format="xml", merge=True)
    print "Config differences..."
    print '-' * 50
    print cfg.diff()

    print "Committing changes..."
    cfg.commit()
    display_static_routes(a_device)

    # Route to discard
    my_route = dict(prefix='1.1.3.0/24', next_hop='10.220.88.1')
    new_route_xml = generate_route_template(my_route)
    print "Configuring static routes using XML... (merge)"
    cfg.load(new_route_xml, format="xml", merge=True)
    print "Config differences..."
    print '-' * 50
    print cfg.diff()
    cfg.rollback(0)
    display_static_routes(a_device)

    cfg.unlock()

if __name__ == "__main__":
    main()
