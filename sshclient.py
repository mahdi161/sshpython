#!/usr/bin/env python
import sys
import getopt
import paramiko
import subprocess

if len(sys.argv) != 5:
       print "Usage: sshclient.py <ip> <port> <user> <password>"
       sys.exit(0)

try:
   ip = str(sys.argv[1])
   port = int(sys.argv[2])
   user = str(sys.argv[3])
   passwd = str(sys.argv[4])
   client = paramiko.SSHClient()
   client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   client.connect(ip, port=port, username=user, password=passwd)
   ssh_session = client.get_transport().open_session()
   paramiko.util.log_to_file("sshclient.log")
   if ssh_session.active:
	print ssh_session.recv(4096)
        
	while 1:
	   try:
                command = raw_input("/>: ").strip('\n')
                if command != 'exit':
	
                    ssh_session.send(command)
		    print ssh_session.recv(4096) + '\n'
		    
                else:
                    ssh_session.send('exit')
                    print 'Closing connection ...'
		    client.close()
                    ssh_session.close()
                    raise Exception('exit')
           except Exception, e:
	      ssh_session.send(str(e))
	client.close()
    
except:
   client.close()

