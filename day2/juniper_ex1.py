#!/usr/bin/env python
"""Using Juniper's pyez for get interface operations."""
from getpass import getpass

from jnpr.junos import Device
from jnpr.junos.op.ethport import EthPortTable

def main():
    """Using Juniper's pyez for get interface operations."""
    password = getpass()
    a_device = Device(host='184.105.247.76', user='pyclass', password=password)
    a_device.open()

    eth = EthPortTable(a_device)
    eth.get()
    print
    for intf, v in eth.items():
        if intf == 'fe-0/0/7':
            print 'intf {}: '.format(intf)
            for field_name, field_value in v:
                if 'bytes' in field_name:
                    print "    {:<15} {:<30}".format(field_name, field_value)
    print

if __name__ == "__main__":
    main()
