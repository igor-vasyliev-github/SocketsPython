import socket
import thread

sHost = '192.168.12.174'
nPort = 22222
listClientSockets = []

def InformAboutAllConnectedClients():
	print '\n\nAll connected clients: ' + str(len(listClientSockets))
	for sock in listClientSockets:
		print sock.getsockname()[0] + ':' + str(sock.getsockname()[1])
	print '\n'

def SendMessageToClientsExceptSpecified(clientSocket, sMessage):
	for curSocket in listClientSockets:
		if clientSocket == curSocket:
			continue
		curSocket.send(sMessage)

#THREAD
def ThreadListenClient(socket , sIP, nPort):
	'''
	thread for receiving messages from each client
	'''
	print '\nCLIENT ' +  sIP + ':' + str(nPort) + ' started thread for listening client'

	socket.send('Thank you for connecting. I\'m server')
	#print '-> Client ' +  sIP + ':' + str(nPort) + ' Thank you for connecting. I\'m server'

	while True:
		sMessage = socket.recv(1024)
		if sMessage == '':
			print 'Socket ' +  sIP + ':' + str(nPort) + ' was disconnected'
			listClientSockets.remove(socket)
			#InformAboutAllConnectedClients()
			break

		# prepating the message to everyone
		sMessageToAllClients = '\nCLIENT ' +  sIP + ':' + str(nPort) + ' said:\n' + sMessage + '\n'
		print sMessageToAllClients

		# send message to all clients, except current
		SendMessageToClientsExceptSpecified (socket, sMessageToAllClients)

#THREAD
def ThreadWaitingNewClients():
	'''
	thread for wait new connections from Clients
	'''
	# Create a socket object
	socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	#host = socket.gethostname() # Get local machine name
	#binds address (hostname, port number pair) to socket.
	socketServer.bind((sHost, nPort))

	# the maximum value is system-dependent (usually 5),
	socketServer.listen(5)

	while True:
		print '\nSERVER: waiting for a new client at ' +  sHost + ':' + str(nPort)
		socketClient, ClientAddress = socketServer.accept()     # Establish connection with client.

		print 'New client connected - ' +  ClientAddress[0] + ":" + str(ClientAddress[1])

		#add client to member list
		listClientSockets.append(socketClient)
		#InformAboutAllConnectedClients()

		#run respective thread for receiving messages from client
		thread.start_new_thread(ThreadListenClient, (socketClient, ClientAddress[0], ClientAddress[1]))

def CloseAllSockets():
	print '\n\nClose all connected clients: ' + str(len(listClientSockets))
	for sock in listClientSockets:
		sock.shutdown(1)
		sock.close()
	print '\nClosing Done'


# MAIN
#start thread for socket server
thread.start_new_thread(ThreadWaitingNewClients, ())

#loop for user input
while True:
	sCommand = raw_input('\nenter command: \nq - exit ')
	sCommand = sCommand.lower()
	if 'q' == sCommand:
		# user wants to shut down server - close all sockets
		CloseAllSockets()
		break
	else:
		print 'Wrong command'
