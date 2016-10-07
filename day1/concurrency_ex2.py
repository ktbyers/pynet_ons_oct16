#!/usr/bin/env python
"""Retrieve the config from a set of devices using threads."""
from datetime import datetime
import threading

from netmiko import ConnectHandler
from my_devices import device_list


def netmiko_cmd(a_device, cmd):
    """Establish Netmiko connection and execute command. Print output."""
    net_connect = ConnectHandler(**a_device)
    print '-' * 50
    print net_connect.find_prompt()
    print '-' * 50
    output = net_connect.send_command(cmd)
    print "\n\n"
    print '#' * 50
    print output
    print '#' * 50
    print

def main():
    """Retrieve the config from a set of devices using threads."""
    start_time = datetime.now()
    for a_device in device_list:
        if 'juniper' in a_device['device_type']:
            cmd = 'show config'
        else:
            cmd = 'show run'
        my_thread = threading.Thread(target=netmiko_cmd, args=(a_device, cmd))
        my_thread.start()

    main_thread = threading.currentThread()
    for some_thread in threading.enumerate():
        if some_thread != main_thread:
            some_thread.join()

    end_time = datetime.now()
    print "\nElapsed time: {}".format(end_time - start_time)

if __name__ == "__main__":
    main()
