#!/usr/bin/env python3
import threading
from random import randint
import time
import paramiko
from paramiko.ssh_exception import AuthenticationException, SSHException, BadHostKeyException

quit_lab = False


host = "192.168.1.146"
user = 'admin'
pw = 'admin1234'
min_time = 10
max_time = 60

ssh = paramiko.SSHClient()

def check_break():
	global quit_lab
	repeat = True
	while repeat:
		status = raw_input("Enter q to exit Lab: ")
		if status is 'q':
			quit_lab = True
			repeat = False
			print("The script will quit when time runs out on this round")
		else:
			print("invalid entry")

def run_wa_lab5(netconnect):
	radiostatus = 1
	while quit_lab == False:
		random_sleep = randint(min_time,max_time)
		time.sleep(random_sleep)
		netconnect, radiostatus = radio_change(netconnect, radiostatus)
	return(netconnect)

def establish_connection():
	success = 0 
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	try:
		print("Establishing Connection with {}".format(host))
		ssh.connect(host,username=user, password=pw,timeout=10)
		chan = ssh.invoke_shell()
	except AuthenticationException:
		print("Authentication failed on " + host + ", please verify your credentials: %s")
		exit()
	except SSHException as sshException:
		print("Unable to establish SSH connection on " + host + ": %s" % sshException)
		exit()
	except BadHostKeyException as badHostKeyException:
		print("Unable to verify server's host key on " + host + ": %s" % badHostKeyException)
		exit()
	except Exception as e:
		print("Operation error on " + host + ": %s" % e)
		exit()	
	changes = []
	time.sleep(1)
	resp = chan.recv(9999)	
	chan.send('enable\n')
	time.sleep(1)
	resp = chan.recv(9999)
	lines = resp.splitlines()
	apname = lines[-1][:-1]
	chan.send('self\n')
	time.sleep(1)
	resp = chan.recv(9999)
	chan.send('int radio 2\n')
	time.sleep(1)
	resp = chan.recv(9999)
	return(chan)

def radio_change(chan, radiostatus):
	if radiostatus == 1:
		cmd = ("power 30\n")
		radiostatus = 0;
	elif radiostatus == 0:
		cmd = ("power 1\n")
		radiostatus = 1;
	chan.send(cmd + '\n')
	time.sleep(1)
	resp = chan.recv(9999)
	chan.send("commit\n")
	return(chan, radiostatus)
	

def close(netconnect):
		print("** Connection Closed **")
		ssh.close()

def main():
	netconnect = establish_connection() # starts ssh session with AP
	input_thread = threading.Thread(target=check_break) # displays message and allows script to be closed
	input_thread.start()
	run_wa_lab5(netconnect)
	close(netconnect)

if __name__ == '__main__':
	main()
