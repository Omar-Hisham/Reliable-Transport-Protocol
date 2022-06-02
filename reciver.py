from ctypes import sizeof
from socket import *
import time
import random
from datetime import datetime

TimeOut = 0.01
ServerSocket=socket(AF_INET,SOCK_DGRAM)
ServerSocket.bind(('',12000))
ServerSocket.settimeout(TimeOut)

lossRate= 0
Buffer=[]
data = bytearray()
NumberofTransmittedACKs = 0
NumberofTransmittedACKsBytes = 0
NumberofLostPackets = 0
NumberofReceivedBytes = 0
last_rec_pack_time = time.time()
StartingTime = datetime.now()
FileID = 0


while True:
    try:
        message,addr=ServerSocket.recvfrom(8192)

        lossFlage = random.uniform(0,100)

        if lossFlage <= lossRate:
            message=False
            NumberofLostPackets+=1
        while message:
            print(f'packet_ID of recived packet: Binary {message[0:16]}  >>>> integer {int(message[0:16],2)}')
            if (len(Buffer) == 0):
                Buffer.append(message)
                data.extend(Buffer[0][32:-32])


            if (int(message[0:16],2) == int(Buffer[-1][0:16],2)+1):

                Buffer.append(message)
                data.extend(Buffer[-1][32:-32])
                NumberofReceivedBytes +=len(Buffer[-1][32:-32])
            message = False
            

    except:
        t = time.time()
        if len(Buffer) == 0:
            continue
        elif ( float(t) - float(last_rec_pack_time)) >= TimeOut :
            ACK = Buffer[-1][0:16] + Buffer[-1][16:32]

            print(f'ACK_ID: ***** {ACK[0:16]} ***** >>>> integer {int(ACK[0:16],2)}')
            ServerSocket.sendto(ACK,addr)
            last_rec_pack_time = time.time()
            NumberofTransmittedACKs += 1
            NumberofTransmittedACKsBytes += len(ACK)
    
        if Buffer[-1][-32:] == bytes(format(4294967295,'032b'),'UTF-8'):
            EndTime= datetime.now()
            ElapsedTime = (EndTime - StartingTime).total_seconds()
            NumberofReceivedPackets = len(Buffer)

            with open("received.png", "wb") as file:
                file.write(data)

            FileID= Buffer[-1][16:32]
            print("=================================================")
            print(f"Transfer Start Time:  *******  {StartingTime.strftime('%H:%M:%S')} *******")
            print("=================================================")
            print(f"Transfer End Time: *******  {EndTime.strftime('%H:%M:%S')} **********")
            print("=================================================")
            print(f"Elapsed Time in Seconds:   {'%.2f' % ElapsedTime} sec")
            print("=================================================")
            print(f"Number of Transmitted ACKs:   {NumberofTransmittedACKs}")
            print("=================================================")
            print(f"Number of Transmitted ACK Bytes :   {NumberofTransmittedACKsBytes}")
            print("=================================================")
            print(f"Number of Received Packets:   {NumberofReceivedPackets}")
            print("=================================================")
            print(f"Number of Received Bytes (Data):   {NumberofReceivedBytes}")
            print(f"Number of Lost Packets:   {NumberofLostPackets}")
            print("=================================================")
            print(f"Average Transfer Rate (bytes/sec):   {'%.2f' %(NumberofReceivedBytes / ElapsedTime)}")
            print("=================================================")
            print(f"Average Transfer Rate (packets/sec):   {'%.2f' %(NumberofReceivedPackets / ElapsedTime)}")
            print("=================================================")
            print(f"The file with ID {FileID} was recieved correctly and saved as'received.png'")

            exit()
            





