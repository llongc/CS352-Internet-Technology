import numpy as mypy
import threading
import time
import random
import sys

import socket as mysoc

def client():
    try:
        ctors=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))
    
        
  
# Define the port on which you want to connect to the server
    port = 44445
    
    sa_sameas_myaddr = mysoc.gethostbyname(sys.argv[1])
    #mysoc.gethostbyname(mysoc.gethostname())
    #host_name = mysoc.gethostname()
    #print("[C] host name in client is ", host_name)
    #print("[C] ip address in client is ", sa_sameas_myaddr)
# connect to the server on local machine
    server_binding=(sa_sameas_myaddr,port)
    ctors.connect(server_binding) 
    
    
    msg=sys.argv[2]
    #ready to write in output file
    f = open('RESOLVED.txt','w')
    ifconnected=False;
    with open(msg,'r') as file:
        #start to read request line by line
        for line in file:
            #remove new line character if available
            #print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
            if line == "\n":
                line = " "
            if "\n" in line:
                #print("!!!!!!!!!!!!!#")
                line = line[:-1]
           #send to RSserver and receive back
            ctors.send(line.encode('utf-8'))
            r = ctors.recv(3074).decode('utf-8')
            
            
            if "\n" in r:
                r=r[:-1]
            f.write(r)
            f.write('\n')
      
    
    f.close()
    
# close the cclient socket 
    ctors.close() 
    exit() #??
    
t3 = threading.Thread(name='client', target=client)
t3.start()

input("Hit ENTER  to exit")

exit()