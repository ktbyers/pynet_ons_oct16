#!/usr/bin/env python
"""Obtain configuration from set of devices in series."""
from datetime import datetime
from netmiko import ConnectHandler
from my_devices import device_list


def main():
    """Obtain configuration from set of devices in series."""
    start_time = datetime.now()
    for a_device in device_list:
        net_connect = ConnectHandler(**a_device)
        print '-' * 50
        print net_connect.find_prompt()
        print '-' * 50
        if 'juniper' not in net_connect.device_type:
            output = net_connect.send_command("show run")
        else:
            output = net_connect.send_command("show config")
        print "\n\n"
        print '#' * 50
        print output
        print '#' * 50
        print

    end_time = datetime.now()
    print "Elapsed time: {}".format(end_time - start_time)
    print

if __name__ == "__main__":
    main()
