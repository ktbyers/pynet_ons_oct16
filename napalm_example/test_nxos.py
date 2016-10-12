#!/usr/bin/env python
from getpass import getpass
from pprint import pprint as pp

from napalm_base import get_network_driver


ip_addr = '31.220.69.245'
username = 'pyclass'
password = getpass()
optional_args = {}
optional_args['nxos_protocol'] = 'http'
optional_args['port'] = 80

driver = get_network_driver('nxos')
device = driver(ip_addr, username, password, optional_args=optional_args)

print
print(">>>Test device open")
device.open()

print
print(">>>Test get facts")
device_facts = device.get_facts()
pp(device_facts)

print
print(">>>Test get lldp neighbors")
#device_int = device.get_lldp_neighbors()
device_int = device.get_lldp_neighbors_detail()
pp(device_int)

#print
#print ">>>Test get environment"
#env = device.get_environment()
#pp(env)

print
print ">>>Test get bgp neighbors"
bgp_neigh = device.get_bgp_neighbors()
pp(bgp_neigh)

print
print ">>>Load config change (merge) - no commit"
device.load_merge_candidate(filename='nexus-merge.conf')
print device.compare_config()

print
print ">>>Discard config change (merge)"
device.discard_config()
print device.compare_config()

print
print ">>>Load config change (merge) - commit"
device.load_merge_candidate(filename='nexus-merge.conf')
print device.compare_config()
device.commit_config()

# nxos-spine1
