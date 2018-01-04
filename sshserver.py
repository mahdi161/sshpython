#!/usr/bin/env python
import paramiko
import getopt
import threading
import sys
import socket
import subprocess
import getpass
import traceback
from paramiko.py3compat import input
host_key = paramiko.RSAKey(filename='test_rsa.key')
username = ''
passwd = ''  

if username == '':
   default_username = getpass.getuser() 
   username = input('username [%s]: ' % default_username)
if len(username) == 0:
   username = default_username
if passwd == '':
   passwd = input('Password:')

class Server(paramiko.ServerInterface):

    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if (username == username) and (password == passwd):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

def main():
 
    if not len(sys.argv[1:]):
        print "Usage: ssh_server.py <server> <port>"
        sys.exit(0)

    server = sys.argv[1]
    ssh_port = int(sys.argv[2])
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((server, ssh_port))
        sock.listen(100)
        print('Listening for connection ...')
        client, addr = sock.accept()
    except Exception as e:
        print('*** Listen/accept failed: ' + str(e))
        sys.exit(1)
    print('Got a connection!')

    try:
       t = paramiko.Transport(client)
       t.add_server_key(host_key)
       paramiko.util.log_to_file("sshserver.log")
       server = Server()
       try:
          t.start_server(server=server)
       except paramiko.SSHException:
          print('SSH negotiation failed')
	  sys.exit(1)

       chan = t.accept(20)
       chan.send("Connected...")
       while 1:
	   command = chan.recv(4096)
	   try:
	      cmd_output = subprocess.check_output(command, shell=True) 
	      chan.send(cmd_output)
           except KeyboardInterrupt:
	       chan.close()

    except Exception, e:
 
        print "Exit: " + str(e)
        try:
            chan.close()
        except:
            pass
        sys.exit(1)

if __name__ == '__main__':
    main()
