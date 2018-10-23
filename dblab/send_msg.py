import socket
import sys


if __name__ == '__main__':

	
	serverIp = sys.argv[1]
	message = 'hihi'

	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	#  sock.bind((Ip, 0))

	sock.connect((serverIp, 7429))

	send_msg = bytes(message, encoding='utf-8')
	sock.send(send_msg)

	print('send : {0}'.format(send_msg))

			
