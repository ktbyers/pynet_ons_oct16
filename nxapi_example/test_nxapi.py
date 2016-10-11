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
