#!/usr/bin/env python
"""
Retrieve the config from a set of devices using threads.
Use queue to pass data back to main thread.
"""
from datetime import datetime
import threading
import Queue

from netmiko import ConnectHandler
from my_devices import device_list


def netmiko_cmd(a_device, cmd, output_q):
    """Establish Netmiko connection and execute command. Print output."""
    net_connect = ConnectHandler(**a_device)
    hostname = net_connect.find_prompt()
    hostname = hostname.rstrip('#')
    hostname = hostname.rstrip('>')
    output = net_connect.send_command(cmd)
    output_q.put({hostname: output})


def main():
    """
    Retrieve the config from a set of devices using threads.
    Use queue to pass data back to main thread.
    """
    start_time = datetime.now()
    output_q = Queue.Queue()
    for a_device in device_list:
        if 'juniper' in a_device['device_type']:
            cmd = 'show config'
        else:
            cmd = 'show run'
        my_thread = threading.Thread(target=netmiko_cmd, args=(a_device, cmd, output_q))
        my_thread.start()

    main_thread = threading.currentThread()
    for some_thread in threading.enumerate():
        if some_thread != main_thread:
            some_thread.join()

    while not output_q.empty():
        my_dict = output_q.get()
        for hostname, config in my_dict.iteritems():
            print
            print '-' * 50
            print hostname
            print '-' * 50
            print
            print '#' * 50
            print config
            print '#' * 50
            print

    end_time = datetime.now()
    print "\nElapsed time: {}".format(end_time - start_time)

if __name__ == "__main__":
    main()
