# Python TCP Client A
import socket 
import time

host = '0.0.0.0'
port = 2004
BUFFER_SIZE = 2000 

udpClientA = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

#udpClientA.connect((host, port))
conn_MESSAGE="sent:hi"
MESSAGE="Delivered!"
s_data=conn_MESSAGE.encode('utf-8') 
udpClientA.sendto(s_data,(host,port))
print(conn_MESSAGE)

data=udpClientA.recvfrom(BUFFER_SIZE)
r_str=data[0].decode('utf-8')
print(r_str)

r1_data=udpClientA.recvfrom(BUFFER_SIZE)
r1_str=r1_data[0].decode('utf-8')
print("received:",r1_str)

while (r1_str)!= "all done!": #till all deliveries completed...
    print("deliver to:",r1_str)
    r2_data=udpClientA.recvfrom(BUFFER_SIZE)
    print("received time:",r2_data[0])
    time.sleep(int(r2_data[0]))
    s_data=MESSAGE.encode('utf-8')
    udpClientA.sendto(s_data,(host,port))   
    r1_data = udpClientA.recvfrom(BUFFER_SIZE)
    r1_str=r1_data[0].decode('utf-8')
  
print("all done!")

udpClientA.close() 
