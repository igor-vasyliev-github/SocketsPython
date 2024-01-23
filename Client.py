import socket
import thread
from sys import exit

sHost = '192.168.12.174'
nPort = 22222
bSocketIsClosed = False

def ThreadMessagesFromServer( socket ):
	'''
	thread for write to console messages from Server
	'''
	print 'started thread for listening server'

	while True:
		sMessage = socket.recv(1024)
		if sMessage == '':
			print "Client was disconnected from server. Server was down."
			socket.shutdown(1)
			socket.close()
			break
		print 'SERVER said: \n' + sMessage

		print '\nenter command: \nm - new message to server\nq - exit '

	#indication, that thread is finished
	global bSocketIsClosed
	bSocketIsClosed = True
	print "bSocketIsClosed = True"

# Create a socket object
socketClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#host = socket.gethostname() # Get local machine name

#connect to server
socketClient.connect((sHost, nPort))

# run separate thread for listening server's messages
thread.start_new_thread(ThreadMessagesFromServer, (socketClient, ))

#send greeting data to server
socketClient.send('Hello, I\'m a new client')
print '-> server: Hello, I\'m a new client'

while True:
	sCommand = raw_input('\nenter command: \nm - new message to server\nq - exit ')
	sCommand = sCommand.lower()
	if 'm' == sCommand:
		sText = raw_input('Please enter your message: ')
		socketClient.send(sText)
	elif 'q' == sCommand:
		# user wants to exit - close socket from client side
		print 'Closing socket and exit'
		if False == bSocketIsClosed:
			socketClient.shutdown(1)
			socketClient.close()
		break
	else:
		print 'Wrong command'
