#!/usr/bin/env python
"""Retrieve the config from a set of devices using processes."""
from datetime import datetime
from multiprocessing import Process

from netmiko import ConnectHandler
from my_devices import device_list


def netmiko_cmd(a_device, cmd):
    """Establish Netmiko connection and execute command. Print output."""
    net_connect = ConnectHandler(**a_device)
    prompt = net_connect.find_prompt()
    output = net_connect.send_command(cmd)
    print '-' * 50
    print prompt
    print '-' * 50
    print "\n\n"
    print '#' * 50
    print output
    print '#' * 50
    print

def main():
    """Retrieve the config from a set of devices using processes."""
    start_time = datetime.now()

    procs = []
    for a_device in device_list:
        if 'juniper' in a_device['device_type']:
            cmd = 'show config'
        else:
            cmd = 'show run'
        my_proc = Process(target=netmiko_cmd, args=(a_device, cmd))
        my_proc.start()
        procs.append(my_proc)

    for a_proc in procs:
        a_proc.join()

    end_time = datetime.now()
    print "\nElapsed time: {}".format(end_time - start_time)

if __name__ == "__main__":
    main()
