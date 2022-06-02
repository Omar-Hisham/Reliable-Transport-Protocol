from ast import Break
from bdb import Breakpoint
import math
from socket import*
import sys
import matplotlib.pylab as plt
from datetime import datetime
from random import randbytes

def read_Div (Mss,filename):
    try:
      with open((filename), "rb") as imagefile:
        data = imagefile.read()

    except:
        print('file does not exist!!! please enter valid file name')
    appDataSize = Mss-64
    packetNo = math.ceil(data.__sizeof__()/appDataSize)
    dataChunk = []
    for i in range(packetNo):
        dataChunk.append(data[i*appDataSize:(i+1)*appDataSize])
    
    return dataChunk

def creatPackets (sPacketID,fileID,datachunks):

    
    packets=[]

    for i in (datachunks):
        if i == datachunks[-1]:
            trailer = bytes(format(4294967295, '032b'), 'UTF-8')
        else:
            trailer = bytes(format(0, '032b'), 'UTF-8')
        appData=i
        file_id=bytes(format(fileID,'016b'),'UTF-8')
        packet_ID = bytes(format(sPacketID, '016b'), 'UTF-8')
        sPacketID += 1
        packet= packet_ID + file_id  + appData + trailer
        packets.append(packet)


        
    return packets

####### attacking scenario  #######

def Attack():
    print("XXXXXXXXXXXXXXXXX Attacking scenario XXXXXXXXXXXXXXXXXX \n")
    print('''
                    uuuuuuu
                uu$$$$$$$$$$$uu
            uu$$$$$$$$$$$$$$$$$uu
            u$$$$$$$$$$$$$$$$$$$$$u
            u$$$$$$$$$$$$$$$$$$$$$$$u
        u$$$$$$$$$$$$$$$$$$$$$$$$$u
        u$$$$$$$$$$$$$$$$$$$$$$$$$u
        u$$$$$$"   "$$$"   "$$$$$$u
        "$$$$"      u$u       $$$$"
            $$$u       u$u       u$$$
            $$$u      u$$$u      u$$$
            "$$$$uu$$$   $$$uu$$$$"
            "$$$$$$$"   "$$$$$$$"
                u$$$$$$$u$$$$$$$u
                u$"$"$"$"$"$"$u
    uuu        $$u$ $ $ $ $u$$       uuu
    u$$$$        $$$$$u$u$u$$$       u$$$$
    $$$$$uu      "$$$$$$$$$"     uu$$$$$$
    u$$$$$$$$$$$uu    """""    uuuu$$$$$$$$$$
    $$$$"""$$$$$$$$$$uuu   uu$$$$$$$$$"""$$$"
    """      ""$$$$$$$$$$$uu ""$"""
            uuuu ""$$$$$$$$$$uuu
    u$$$uuu$$$$$$$$$uu ""$$$$$$$$$$$uuu$$$
    $$$$$$$$$$""""           ""$$$$$$$$$$$"
    "$$$$$"                      ""$$$$""
        $$$"                         $$$$"

    ''')

    fakeID = 0
    fakeFile = 111
    while True:
        ftrailer = bytes(format(0, '032b'), 'UTF-8')
        fappData=randbytes(Mss - 64)
        ffile_id=bytes(format(fakeFile,'016b'),'UTF-8')
        fpacket_ID = bytes(format(fakeID, '016b'), 'UTF-8')
        fakeID += 1
        fpacket= fpacket_ID + ffile_id  + fappData + ftrailer
        Client_socket.sendto(fpacket, (IP, int(portNo)))

    
###### system param ###########

fileName = sys.argv[1]
windowSize = 30
timeout = 0.01
Mss = 2048
IP='localhost'
portNo = 12000
chunks = read_Div(Mss, fileName)
print(fileName)
packets = creatPackets(0, 1, chunks)
Client_socket = socket(AF_INET, SOCK_DGRAM)
Client_socket.settimeout(timeout)
startW = 0
endW = lastendw = 0
StartingTime = datetime.now()
TransmitedPacketsTimeLine= []
TransmitedPacketsIDs= []
ReTransmitedPacketsTimeLine= []
ReTransmitedPacketsIDs= []
NumberOfBytes = 0
message = False

#Attack()  ####### attacking scenario  #######

######## teansmossion loop ##########
while startW < (len(packets)):
    endW= startW + windowSize

    if endW >= len(packets):
        endW = len(packets)

    if endW != lastendw or message  :
        lastendw = endW
        for i in range(startW,endW):
            print(f'packet_ID of transimitted packet: Binary {packets[i][0:16]}  //// integer {int(packets[i][0:16],2)}  ')
            Client_socket.sendto(packets[i], (IP, int(portNo)))

            SendingTime = (datetime.now() - StartingTime).total_seconds()    
            NumberOfBytes +=len(packets[i])
            if int(packets[i][0:16],2) in TransmitedPacketsIDs :
                ReTransmitedPacketsTimeLine.append(SendingTime)
                ReTransmitedPacketsIDs.append(int(packets[i][0:16],2))
            else:
                TransmitedPacketsTimeLine.append(SendingTime)
                TransmitedPacketsIDs.append(int(packets[i][0:16],2))


    try:
        message, addr = Client_socket.recvfrom(8192)
        startW = int(message[0:16],2)+1
        

    except:
        message = False
    if startW >= (len(packets)-1):
        break

EndTime= datetime.now()
ElapsedTime = (EndTime - StartingTime).total_seconds()


print("===============================================================")
print(f" Timeout = {timeout} seconde //// Window Size = {windowSize} ////  MSS = {Mss} ")
print("===============================================================")
print(f"Transfer Start Time:  *******  {StartingTime.strftime('%H:%M:%S')} *******")
print("===============================================================")
print(f"Transfer End Time: *******  {EndTime.strftime('%H:%M:%S')} **********")
print("===============================================================")
print(f"Elapsed Time in Seconds:   {'%.2f' % ElapsedTime} sec")
print("===============================================================")
print(f"Number of Packets:  ********* {len(TransmitedPacketsIDs)} *********")
print("===============================================================")
print(f"Number of Bytes:  ******** {NumberOfBytes}*********")
print("===============================================================")
print(f"Number of Retransmitted Packets:   *******{len(ReTransmitedPacketsIDs)}**********")
print("===============================================================")
print(f"Average Transfer Rate (bytes/sec):   ********{'%.2f' %(NumberOfBytes / ElapsedTime)}*******")
print("===============================================================")
print(f"Average Transfer Rate (packets/sec): ********  {'%.2f' %(len(packets) / ElapsedTime)} *******")
print("===============================================================")


NumberOfPackets = len(packets)
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.scatter(TransmitedPacketsTimeLine, TransmitedPacketsIDs, s=10, c='g', marker="s", label='Sent Packets')
ax1.scatter(ReTransmitedPacketsTimeLine, ReTransmitedPacketsIDs, s=10, c='r', marker="o", label='Resent Packets')
plt.legend(loc='upper right')
plt.text(0,NumberOfPackets , "Number of retransmissions: "+str(len(ReTransmitedPacketsIDs))+" packets")
plt.text(0,NumberOfPackets* 0.9,"Window Size: "+str(windowSize)+" packets")
plt.text(0,NumberOfPackets* 0.8,"MSS: "+str(Mss)+" bytes")
plt.text(0,NumberOfPackets* 0.6,"Timeout: "+str(timeout)+" seconds")
plt.text(0,NumberOfPackets* 0.4,"Loss Rate: "+str(int(len(ReTransmitedPacketsIDs)/NumberOfPackets*100))+" %")
plt.xlabel("Time since transmission started in secondes")
plt.ylabel("Packet ID")
plt.show()
exit()






