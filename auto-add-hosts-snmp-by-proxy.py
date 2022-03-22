#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#author: Janssen dos Reis Lima

import sys
import logging
from pyzabbix import ZabbixAPI
import csv
from progressbar import ProgressBar, Percentage, ETA, ReverseBar, RotatingMarker, Timer

##PARA DEBUG CASO QUEIRA
#stream = logging.StreamHandler(sys.stdout)
#stream.setLevel(logging.DEBUG)
#log = logging.getLogger('pyzabbix')
#log.addHandler(stream)
#log.setLevel(logging.DEBUG)

zapi = ZabbixAPI("http://localhost/zabbix")
zapi.login(user="suporte", password="123Mud@r")

# Disable SSL certificate verification
zapi.session.verify = False

# Specify a timeout (in seconds)
zapi.timeout = 5.1

arq = csv.reader(open('/tmp/hosts.csv'))

linhas = sum(1 for linha in arq)

f = csv.reader(open('/tmp/hosts.csv'), delimiter=';')
bar = ProgressBar(maxval=linhas,widgets=[Percentage(), ReverseBar(), ETA(), RotatingMarker(), Timer()]).start()
i = 0

for [hostname,ip] in f:
    hostcriado = zapi.host.create(
        host= hostname,
        proxy_hostid= 10731,
        status= 0,
        interfaces=[{
            "type": 2,
            "main": "1",
            "useip": 1,
            "ip": ip,
            "dns": "",
            "port": 161,
            "details": {
                 "version": 2,
                 "bulk": "1",
                 "community": "{$SNMP_COMMUNITY}"
            }
        }],
        groups=[{
            "groupid": 40
        }],
        templates=[{
            "templateid": 10712
        }],
        macros=[{
            "macro": "{$SNMP_COMMUNITY}",
            "value": "Fw56Ty34"
        }]
    )


    i += 1
    bar.update(i)

bar.finish
print()
