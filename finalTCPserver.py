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
            status_truck1=0 #making truck unavailable
            task_done+=1
            delivery_info(1,trucks[0],loc_list[task_done-1],time_list[task_done-1])
            
            status_truck2=0
            task_done+=1
            delivery_info(2,trucks[1],loc_list[task_done-1],time_list[task_done-1])
                
            status_truck3=0
            task_done+=1
            delivery_info(3,trucks[2],loc_list[task_done-1],time_list[task_done-1])
                
            trucks[0].settimeout(1)#to wait for 1 sec to receive message, if not move on to the next 
            trucks[1].settimeout(1)
            trucks[2].settimeout(1)
            
            #for the remaining locations.....
            while task_done<len(loc_list):
            
                while (status_truck1!=1 or status_truck2!=1 or status_truck3!=1):
                    try:
                        r1_data=trucks[0].recv(2048)
                        r1_data.decode('utf-8')
                        status_truck1=1 #making truck available for next delivery 
                        print("truck 1:"+str(r1_data)+"ready for next...")
                        break
                        
                    except socket.timeout:
                        try:
                            r2_data=trucks[1].recv(2048)
                            r2_data.decode('utf-8')
                            status_truck2=1
                            print("truck 2:"+str(r2_data)+"ready for next...")
                            break
                      
                        except socket.timeout:
                            try:
                                r3_data=trucks[2].recv(2048)
                                r3_data.decode('utf-8')
                                status_truck3=1
                                print("truck 3:"+str(r3_data)+"ready for next...")
                                break
                            except:
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

    if task_done==(len(loc_list)):#if all tasks done
        MESSAGE="all done!"
        trucks[0].settimeout(None)
        trucks[1].settimeout(None)
        trucks[2].settimeout(None)
        
        if(status_truck3==0):
            r3_data=trucks[2].recv(2048)
            r3_data.decode('utf-8')
            print("truck 3:",r3_data)
        
        if(status_truck2==0):
            r2_data=trucks[1].recv(2048)
            r2_data.decode('utf-8')
            print("truck 2:",r2_data)
        
        if(status_truck1==0):
            r1_data=trucks[0].recv(2048)
            r1_data.decode('utf-8')
            print("truck 1:",r1_data)   
            
        s_data=MESSAGE.encode('utf-8')
        for i in range(0,len(trucks)):
            #send all done message to trucks
            trucks[i].send(s_data)
        print(MESSAGE)


def delivery_info(truck_no,truck,loc,timee):
    st=""
    st=str(loc)+" Truck "+str(truck_no)
    #writing location to output file
    file=open('/home/anika/truck.txt','a')
    file.write(st)
    file.close()
            
    #to append new line to file
    file=open('/home/anika/truck.txt','a')
    file.write('\n')
    file.close() 
    
    MESSAGE=str(loc)
    s1_data=MESSAGE.encode('utf-8')
    truck.send(s1_data) #echo send location to truck
    time.sleep(2)
    time1=str(timee) 
    s2_data=time1.encode('utf-8')
    truck.send(s2_data) #send time to truck

# Multisocket Python server : TCP Server Socket
TCP_IP = '0.0.0.0' 
TCP_PORT = 2004 

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpServer.bind((TCP_IP, TCP_PORT))
trucks = [] 

while True:
    tcpServer.listen(4) 
    print("Multiclient Python server : Waiting for connections from TCP clients...") 
    (conn,addr) = tcpServer.accept()
    print("[+] New server socket started for:" + str(addr))
    trucks.append(conn)       #list of sockets
    count+=1
    mes="hi!Truck "+str(count)
    s_data=mes.encode('utf-8')
    trucks[count-1].send(s_data)
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
       
