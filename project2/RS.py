import  numpy as mypy
import threading
import time
import random
import sys 

import socket as mysoc

def server():
    
    comhost = sys.argv[1]
    eduhost = sys.argv[2]
    table = sys.argv[3]
    
    try:
        rssd=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        #print("[S]: Server socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))
    
    try:
        rsedu=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        #print("[S]: Server socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))
    
    try:
        rscom=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        #print("[S]: Server socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))
    
    server_binding=(comhost,50020)
    rscom.connect(server_binding)
    
    server_binding=(eduhost,50010)
    rsedu.connect(server_binding)
    
    server_binding=('',44445)
    rssd.bind(server_binding)
    rssd.listen(1)
    host=mysoc.gethostname()
    #print("[S]: Server host name is: ",host)
    localhost_ip=(mysoc.gethostbyname(host))
    #print("[S]: Server IP address is  ",localhost_ip)
    csockid,addr=rssd.accept()
    #print ("[S]: Got a connection request from a client at", addr)
    
    
    while True:
        
        # receive a string contain hostname from the client
        hostNameStr = csockid.recv(3074).decode('utf-8')
        #print("receive a line from client: ",hostNameStr)
    
        if hostNameStr == "":
            #print ("finished")
            break;
        else:
            #RS does a look up in the DNS_table
            #if there is a match, sends the entry as a string "Hostname IPaddess A"

            #read the DNS_table 
            sendBackMsg = "?"
            
            with open(table, 'r') as DNSfile:
                for line in DNSfile:
                    breakIntoArray = line.split()
                    if len(breakIntoArray) < 3:
                        continue
                    if breakIntoArray[2] != "A":
                        NSname = line
                        #just in case if the TS server name is not in stored in the last line 
                        #of the DNSTS_table

                    if breakIntoArray[0] == hostNameStr:
                        sendBackMsg = line
                        csockid.send(sendBackMsg.encode('utf-8'))
                        break
                #print("-----cannot found in root server table, next step: ")
                #print("hostName is ",hostNameStr)
            if(sendBackMsg == "?"):
                
                if(hostNameStr.endswith(".com")):
                    #print("22222")
                    rscom.send(hostNameStr.encode('utf-8'))
                    s = rscom.recv(3074).decode('utf-8')
                    csockid.send(s.encode('utf-8'))
                    
                elif(hostNameStr.endswith(".edu")):
                    
                    rsedu.send(hostNameStr.encode('utf-8'))
                    s = rsedu.recv(3074).decode('utf-8')
                    csockid.send(s.encode('utf-8'))
                else:
                    
                    s="Error:HOST NOT FOUND."
                    csockid.send(s.encode('utf-8'))
                 

            DNSfile.close()
            
    rssd.close()
    rscom.close()
    rsedu.close()
    exit()


t2 = threading.Thread(name='server', target=server)
t2.start()
time.sleep(random.random()*5)