#!/usr/bin/env python
"""
https://www.juniper.net/techpubs/en_US/junos-pyez1.0/topics/concept/junos-pyez-tables-and-views-overview.html
"""

from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.op.lldp import LLDPNeighborTable
from jnpr.junos.op.ethport import EthPortTable
from jnpr.junos.op.routes import RouteTable
from jnpr.junos.exception import LockError

from getpass import getpass
from pprint import pprint

password = getpass() 
a_device = Device(host='184.105.247.76', user='pyclass', password=password)
print a_device.open()
a_device.timeout = 300

#### Facts
pprint(a_device.facts)

#### Getter operations
print "\nLLDP Get"
print '-' * 50
lldp = LLDPNeighborTable(a_device)
lldp.get()

for k, v in lldp.items():
    print k
    for entry in v:
        print entry

#### Getter operations
print "\nEth Port Get"
print '-' * 50
eth = EthPortTable(a_device)
eth.get()
pprint(eth.items())

#### Getter operations
print "\nRoute Table Get"
print '-' * 50
z_routes = RouteTable(a_device)
z_routes.get()
pprint(z_routes.items())

#### Config operations
print
print "Current static routes"
print '-' * 50
pprint(z_routes.keys())
print

# Create config object
cfg = Config(a_device)
cfg.lock()

config_str = """
routing-options {
    static {
        route 1.1.1.0/24 next-hop 10.220.88.1;
        route 1.1.2.0/24 next-hop 10.220.88.1;
        route 1.1.3.0/24 next-hop 10.220.88.1;
    }
} 
"""

cfg.load(config_str, format="text", merge=True)
#cfg.load(path=config_file, format="text", merge=True)
print "Config differences..."
print '-' * 50
print cfg.diff()

print "Committing changes..."
print '-' * 50
cfg.commit(comment="Testing commit using PyEZ,Oct9")

z_routes.get()
print "Current static routes"
print '-' * 50
pprint(z_routes.keys())

print "Testing replace operation (conf)..."
config_str = """
routing-options {
    replace:
    static {
        route 0.0.0.0/0 next-hop 10.220.88.1;
    }
} 
"""

cfg.load(config_str, format="text", merge=False)
print "Config differences..."
print '-' * 50
print cfg.diff()

print "Committing changes..."
print '-' * 50
cfg.commit(comment="Testing commit using PyEZ, Oct9")

z_routes.get()
print "Current static routes"
print '-' * 50
pprint(z_routes.keys())

config_xml = """
<configuration>
        <system>
            <host-name>test-srx1</host-name>
        </system>
</configuration>
"""
#            <host-name>juniper-srx</host-name>
print "Testing xml..."
cfg.load(config_xml, format="xml", merge=True)
print "Config differences..."
print '-' * 50
print cfg.diff()

print "Rolling back..."
cfg.rollback(0)
print "Config differences..."
print '-' * 50
print cfg.diff()

cfg.load(config_str, format="text", merge=False)
print "Config differences..."
print '-' * 50
print cfg.diff()

print "Committing changes..."
print '-' * 50
cfg.commit(comment="Testing commit using PyEZ, Oct9")

cfg.unlock()
