#!/usr/bin/env python
from ciscoconfparse import CiscoConfParse

if __name__ == "__main__":
    cisco_file = 'cisco_config.txt'

    cisco_cfg = CiscoConfParse(cisco_file)
    intf_obj = cisco_cfg.find_objects(r"^interf")

#    for c_map in crypto_maps:
#        print
#        print c_map.text
#        for child in c_map.children:
#            print child.text
#    print
