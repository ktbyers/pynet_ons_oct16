#!/usr/bin/env python
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from pprint import pprint

from pynxos.device import Device

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)



if __name__ == "__main__":
    nexus_ip = "85.190.182.85"
    nxs_test = Device(host=nexus_ip, username="pyclass", password="88newclass",
                      transport='https', port=8443)

    #### FACTS
    print "\nFacts"
    print '-' * 50
    pprint(nxs_test.facts)

    ###### SHOW
    print "\nShow"
    print '-' * 50
    print nxs_test.show("show hostname")
    print nxs_test.show("show ip arp vrf management", raw_text=True)
    pprint(nxs_test.show("show ip arp vrf management", raw_text=False))

    ##### CONFIG
    print "\nConfig"
    print '-' * 50
    nxs_test.config("hostname test123")
    print nxs_test.show("show hostname")

    nxs_test.config("hostname nxos-spine2")
    print nxs_test.show("show hostname")
    print

    
