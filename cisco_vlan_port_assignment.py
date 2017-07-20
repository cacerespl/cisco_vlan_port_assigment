"""

This script change the vlan number of a port on a Cisco switch 3750 
The user should give the IP address of the host connected to that port.

"""


import paramiko
import time
import re
import sys
import smtplib

ip = sys.argv[1]
vlan = sys.argv[2]
username = sys.argv[3]
password = sys.argv[4]
switch_ip = sys.argv[5]

#Connecting to the switch
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(switch_ip, username=username, password=password, allow_agent=False, look_for_keys=False)
ssh_conn=ssh.invoke_shell()
ssh_conn.send("\n")
time.sleep(1)
output = ssh_conn.recv(10000)


def get_mac(ip):
    ssh_conn.send("show ip arp "+ip+"\n")
    time.sleep(2)
    output = ssh_conn.recv(10000)
    mac_add = re.findall(r'[0-f][0-f][0-f][0-f]\.[0-f][0-f][0-f][0-f]\.[0-f][0-f][0-f][0-f]',output)
    return mac_add[0]
    
def get_interface(mac):
    ssh_conn.send("show mac address-table add "+mac+"\n")
    time.sleep(2)
    output = ssh_conn.recv(10000)
    port = re.findall(r'Gi.*',output)
    interface = port[0].rstrip()   
    return interface

def configuring_interface(interface):
    ssh_conn.send("conf t\n")
    time.sleep(2)
    ssh_conn.send("interface "+interface+"\n")
    time.sleep(2)
    ssh_conn.send("switchport access vlan "+vlan+"\n")
    time.sleep(2)

#Running functions
mac = get_mac(ip)
print 'The mac address of the host is %s' %mac
port = get_interface(mac)
print 'The host is located in port: '+port
configuring_interface(port)
	

ssh.close()

