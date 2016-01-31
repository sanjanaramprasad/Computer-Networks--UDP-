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

host = sys.argv[2]
server_port = int(sys.argv[4])
client_port=int(sys.argv[6])
c=socket(AF_INET,SOCK_DGRAM)
c.bind(('',client_port))
message=sys.argv[8]
c.sendto(message,(host,server_port))
message,address=c.recvfrom(2048)
print("The message received from the server is :",message)
print ("")
c.close()





ip_header = {}


#calculates and stores all the required ip headers
def checksum_calculation(ip_header):
	sum=0

        #'''computes the sum of all the header values'''
	for i in range(0,len(ip_header)):
		sum=sum+int(ip_header[i],16)#10
		z=sum
	final_sum=hex(sum)
	print("The Addition of values is : ",final_sum)
	m=""
	p="0x"

        '''checks if there is any carry in the sum,if there is the carry is wrapped around i.e. added back to the sum without carry'''
	if len(final_sum)>6:
		for z in range(0,len(final_sum)-6):
			p=p+final_sum[z+2]
			l=final_sum[z+2]
			m=final_sum.replace(l,"")
	sum_nocarry=int(m,16)
	carry=int(p,16)
	final_checksum=sum_nocarry+carry
	print "With wrap around : ",hex(final_checksum)

        ''' finds 1's complement of the computed checksum with wrap around'''
	checksum1=hex(final_checksum)
	checksum2=(~final_checksum)
	checksum_complement=checksum2 & 0xffff
	print "1's complement : ",hex(checksum_complement)
	print ""



#calculates and stores all the required ip headers
def checksum_computation(server_ip,client_ip,server_port,client_port,data):
	server_split=server_ip.split('.')
	client_split=client_ip.split('.')
        
	i=0
	while i<4:
		server_split[i]=int(server_split[i])
		i=i+1
	ip_header0=format(server_split[0],'02x')+format(server_split[1],'02x')
	ip_header[0]="0x"+ip_header0
	ip_header1=format(server_split[2],'02x')+format(server_split[3],'02x')
	ip_header[1]="0x"+ip_header1
	j=0
	while j<4:
		client_split[j]=int(client_split[j])
		j=j+1
        #print(client_split)
	ip_header2=format(client_split[0],'02x')+format(client_split[1],'02x')
	ip_header[2]="0x"+ip_header2
	ip_header3=format(client_split[2],'02x')+format(client_split[3],'02x')
	ip_header[3]="0x"+ip_header3
	ip_header[4]=hex(17)
	data_len=len(data)
	UDP_length=8+data_len
	UDP_len=hex(UDP_length)
	ip_header[5]=UDP_len
	ip_header[8]=UDP_len
	server_porth=hex(server_port)
	ip_header[6]=server_porth
	client_porth=hex(client_port)
	ip_header[7]=client_porth
	print" Server IP address(first 2 bytes) : ",ip_header[0]
	print" Server IP address(last 2 bytes)  :  ",ip_header[1]
	print" Client IP address(first 2 bytes)  :  ",ip_header[2]
	print" Client IP address(last 2 bytes)  :  ",ip_header[3]
	print" Protocol Number :  ",ip_header[4]
	print" UDP Length :  ",ip_header[5]
	print" Server Port number  :  ",ip_header[6]
	print" Server Port number  :  ",ip_header[7]
	print" UDP Length  :  ",ip_header[8]
        #print(ip_header)
	list_data=[hex(ord(c)) for c in data]#gets ascii value in hex of all characters in data
        #print(list_data)
	k=0
	list_data1=[]
	while k<len(data):
		list_data1.append(list_data[k][2:])
		k=k+1
	if(len(list_data1)%2 == 0):#checks if even
		l=0
		m=9#data is stored from index 9 because all indices before this are reserved for ip headers
		for l in range(0,len(list_data1)-1,2):
			ip_header[m]="0x"+list_data1[l]+list_data1[l+1]#appends two charactrs at a time
			print"Data (2 bytes) : ",ip_header[m]
			m=m+1
	else:
		last=len(data)-1
		last_ele=list_data1[last]
		p=0
		q=9
		for p in range(0,len(list_data1)-2,2):
			ip_header[q]="0x"+list_data1[p]+list_data1[p+1]#appends two characters at a time but the last element
			print"Data (2 bytes) : ",ip_header[q]
			q=q+1
		ip_header[q]="0x"+last_ele+"00"#pads the last element with 00
		print"Data (2 bytes) : ",ip_header[q]


        checksum_calculation(ip_header)
#to find the 6 characters
def second_request(data):
	print ""
	list_ascii=[]
	list_hex=[]
	for each in data:
		each=hex(ord(each))
		list_ascii.append(each)
	for i in range(0,4):
		list_hex.append(list_ascii[i][2:])
        #print(list_hex)
	if(len(data)%2==0):
		data=[]#contains the hexadecimal values grouped in two bytes
		data.append("0x"+list_hex[0]+list_hex[1])
		data.append("0x"+list_hex[2]+list_hex[3])
                #print("For even data",data)
	else:
		data=[]#contains the hexadecimal value of the first,all other elements grouped in two bytes and the last element padded with 00
		data.append("0x"+list_hex[0])	
		data.append("0x"+list_hex[1]+list_hex[2])
		data.append("0x"+list_hex[3]+"00")
                #print("For odd data:",data
	sum=0
	for each in data:
		sum=sum+int(each,16)
	total_sum=hex(sum)
        #print(total_sum)
	length=hex(12)
	final_sum=int(total_sum,16)+int(length,16)
	final_sum=hex(final_sum)
	total=0xffff
	characters=total-int(final_sum,16)
        #print(hex(characters))
	chars=hex(characters)#the six characters to be appended
	first="0x"+chars[2:4]
        #print firs
	second="0x"+chars[4:]
	print"The fifth character is :",chr(int(first,16))#the last two characters to be computed
	print"The sixth character is :",chr(int(second,16))
	fifth_char=chr(int(first,16))
	sixth_char=chr(int(second,16))
	for each in list_ascii:
		each="0x"+each
        #print list_ascii
	first_four=""
	for k in range(0,4):
		each1=chr(int(list_ascii[k],16))
		first_four=first_four+each1
	print"The 6 characters to be appended are : ",first_four+fifth_char+sixth_char




print "CHECKSUM COMPUTED IS : \n"
checksum_computation(sys.argv[2],sys.argv[2],int(sys.argv[4]),int(sys.argv[6]),sys.argv[8])
print "SECOND REQUEST : "
second_request(sys.argv[8])
