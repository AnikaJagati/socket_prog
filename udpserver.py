import socket 
import time

count=0

def run1(trucks,loc_list,time_list):
    status_truck1=1#checking availability of each truck
    status_truck2=1
    status_truck3=1
    task_done=0
    while True :
        if len(loc_list)==1:
            task_done+=1
            status_truck1=0
            delivery_info(1,trucks[0],loc_list[0],time_list[0])
            break
       
        elif len(loc_list)==2:
            task_done+=1
            status_truck1=0
            delivery_info(1,trucks[0],loc_list[0],time_list[0])
            task_done+=1
            status_truck2=0
            delivery_info(2,trucks[1],loc_list[1],time_list[1])
            break
        
        else:
            status_truck1=0
            task_done+=1
            delivery_info(1,trucks[0],loc_list[task_done-1],time_list[task_done-1])
            
            status_truck2=0
            task_done+=1
            delivery_info(2,trucks[1],loc_list[task_done-1],time_list[task_done-1])
                
            status_truck3=0
            task_done+=1
            delivery_info(3,trucks[2],loc_list[task_done-1],time_list[task_done-1])
            
            tcpServer.settimeout(1)
            
            #for the remaining locations.....
            while task_done<len(loc_list):
                
                while (status_truck1!=1 or status_truck2!=1 or status_truck3!=1):
                    try:
                        (r_data,addr)=tcpServer.recvfrom(2048)
                        if(addr==trucks[0]):
                            r_data.decode('utf-8')
                            status_truck1=1
                            print("truck 1:"+str(r_data)+"ready for next...")
                            break
                        elif(addr==trucks[1]):
                            r_data.decode('utf-8')
                            status_truck2=1
                            print("truck 2:"+str(r_data)+"ready for next...")
                            break
                        else:
                            r_data.decode('utf-8')
                            status_truck3=1
                            print("truck 3:"+str(r_data)+"ready for next...")
                            break
                        
                    except socket.timeout:
                        continue
                        
                if status_truck1==1:
                    status_truck1=0
                    task_done+=1
                    delivery_info(1,trucks[0],loc_list[task_done-1],time_list[task_done-1])
                
                elif status_truck2==1:
                    status_truck2=0
                    task_done+=1
                    delivery_info(2,trucks[1],loc_list[task_done-1],time_list[task_done-1])
                    if(task_done==len(loc_list)):
                        break
                    
                elif status_truck3==1:
                    status_truck3=0
                    task_done+=1
                    delivery_info(3,trucks[2],loc_list[task_done-1],time_list[task_done-1])
                
            break    

    if task_done==(len(loc_list)):
        MESSAGE="all done!"
        tcpServer.settimeout(None)
        recv_mes=0
        if(status_truck3==0):
            recv_mes+=1
        if(status_truck2==0):
            recv_mes+=1
        if(status_truck1==0):
            recv_mes+=1
       
        for i in range(0,recv_mes):
            (r_data,addr)=tcpServer.recvfrom(2048)
            if(addr==trucks[0]):
                print("truck 1:"+str(r_data))
            if(addr==trucks[1]):
                print("truck 2:"+str(r_data))
            if(addr==trucks[2]):
                print("truck 3:"+str(r_data))    
        
        s_data=MESSAGE.encode('utf-8')
        for i in range(0,len(trucks)):
            tcpServer.sendto(s_data,trucks[i])
    
        print(MESSAGE)   


def delivery_info(truck_no,truck,loc,timee):
    st=""
    st=str(loc)+" Truck "+str(truck_no)
    #writing to output file
    file=open('/home/anika/truck.txt','a')
    file.write(st)
    file.close()
            
    #to append new line to file
    file=open('/home/anika/truck.txt','a')
    file.write('\n')
    file.close() 
    
    MESSAGE=str(loc)
    s1_data=MESSAGE.encode('utf-8')
    tcpServer.sendto(s1_data,truck) #echo
    time.sleep(2)
    time1=str(timee)
    s2_data=time1.encode('utf-8')
    tcpServer.sendto(s2_data,truck)

# Multisocket Python server : TCP Server Socket
TCP_IP = '0.0.0.0' 
TCP_PORT = 2004 

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tcpServer.bind((TCP_IP,TCP_PORT))
trucks = [] 

while True:
    
    print("Python server : Waiting for connections from UDP clients...") 
   
    (r_data,addr)=tcpServer.recvfrom(2048)
    print("[+] New server socket started for:" + str(addr))
    trucks.append(addr)       #list of sockets
    mes="hi!Truck "+str(count+1)
    s_data=mes.encode('utf-8')
    tcpServer.sendto((s_data),trucks[count])
    count+=1 
    if(count==3):
        break

N=int(input("\n enter number of locations:"))#number of locations
L=list()#list of locations
T=list()#list of time durations
for i in range(0,N):
    st=str(input("enter location with estimated time:"))
    x=st.split(' ')
    L.append(x[0])#location list
    T.append(x[1])#time taken for each loc list
    x=[]
print("\n")
run1(trucks,L,T)# passing the info to a function 

       
