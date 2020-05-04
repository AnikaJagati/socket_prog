# Python TCP Client A
import socket 
import time

host = socket.gethostname() 
port = 2004
BUFFER_SIZE = 2000 

tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

tcpClientA.connect((host, port))
data=tcpClientA.recv(BUFFER_SIZE)

print(data)

MESSAGE="Delivered!"

r1_data=tcpClientA.recv(BUFFER_SIZE)
r1_str=r1_data.decode('utf-8')

while (r1_str)!= "all done!": #till all deliveries completed...
    print("deliver to:",r1_str)
    r2_data=tcpClientA.recv(BUFFER_SIZE)
    print("received time:",r2_data)
    time.sleep(int(r2_data))
    s_data=MESSAGE.encode('utf-8')
    tcpClientA.send(s_data)   
    r1_data = tcpClientA.recv(BUFFER_SIZE)
    r1_str=r1_data.decode('utf-8')
  
print("all done!")
tcpClientA.close() 
