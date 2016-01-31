import sys
import getopt

try:
	#argv holds the command line arguements
	opts, args = getopt.getopt(sys.argv,"s:p:P:d")
	#incase there is some error while entering the command line aruements then the following statement is executed.
except getopt.GetoptError as err:
	print("./asn1.py -s <server ip address> -p <server port number> -P<destination port number> -d<data>")
	sys.exit(2)
	

from socket import *

server_port = int(sys.argv[4])
s=socket(AF_INET,SOCK_DGRAM)
s.bind(('',server_port))
print ("The server is ready to receive")

while True:
	data,address=s.recvfrom(2048)
	if data:
		datanew=data*2#duplicates the ata and echoes it back to the client
	s.sendto(datanew,address)
