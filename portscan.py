#!/usr/bin/env python
import socket
import subprocess
import sys
import getopt
import argparse
from datetime import datetime
subprocess.call('clear', shell=True)
try:
    options, remainder = getopt.getopt(sys.argv[1:], 'u:p:', ['url=',])
except getopt.GetoptError as e:
    print (str(e))
    print("Usage: %s -u www.example.com" % sys.argv[0])
    sys.exit(2)
parser = argparse.ArgumentParser(description='portscanner')
parser.add_argument('-u','--url', help='Input url',required=True)
parser.add_argument('-p','--ports', help='Input ports denomination "," Sample: 22,80,443',required=True)
args = parser.parse_args()
for opt, arg in options:
    if opt in ('-u', '--url'):
        url = arg
    elif opt in ('-p', '--ports'):
        ports_list = arg
remoteServer = url
ports = []
if "," in arg:
    try:
        for p in ports_list.split(","):
            if (int(p) <= 65535):
                ports.append(int(p))
            else:
                print "Ports cannot be higher than 65535"
                sys.exit(1)
    except:
        print "Error with port specification. e.g. (22,23,25)"
        sys.exit(1)

else:
    try:
        if (int(arg) <= 65535):
            ports.append(int(arg))
        else:
            print "Ports cannot be higher than 65535"
            sys.exit(1)
    except:
            print "Error with port specified. See help."
            sys.exit(1)

try:
    remoteServerIP  = socket.gethostbyname(remoteServer)
except socket.gaierror as g:
    print 'Hostname could not be resolved. Exiting'
    sys.exit(2)
start = datetime.strftime(datetime.now(),'%b %d %Y %I:%M%p')
print "-" * 60
print "Please wait, scanning remote host", remoteServerIP
print "Scanning started at: {}".format(start)
print "-" * 60
t1 = datetime.now()
try:
        for port in ports:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                result = s.connect_ex((remoteServerIP, int(port)))
                if result == 0:
                    print "Port {0} is open {1}".format(port, remoteServerIP)
                    s.close()
            except:
                    s.close()
except KeyboardInterrupt:
    print "You pressed Ctrl+C"
    sys.exit(2)
except socket.error:
    print "Couldn't connect to server"
    sys.exit(2)
t2 = datetime.now()
total =  t2 - t1
print 'Scanning Completed in: ', total
