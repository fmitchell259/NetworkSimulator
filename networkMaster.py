import random, time, numpy, string
from random import shuffle

nodeList = []
dataType = ['Video','Textfile','Audio','Code','Image','Game Streaming','Download Data']
packetsArrived = []
numberOfNodes = 6
processTime = [0,0.2,0.2,0.2,0.2,1,0.2]

## Fibre Link Limitations ##

fibreLimits = []
for count in range(36):
    fibreLimits.append(0)

oneToTwo = 200      # Index 1
oneToFour = 600     # Index 2
twoToThree = 100    # Index 8
twoToOne = 200      # Index 6
twoToSix = 270      # Index 10
threeToTwo = 100    # Index 13
threeToFive = 450   # Index 16
fourToOne = 600     # Index 18
fourToFive = 800    # Index 22
fourToSix = 900     # Index 23
fiveToThree = 450   # Index 26
fiveToFour = 800    # Index 27
fiveToSix = 470     # Index 29
sixToTwo = 270      # Index 31
sixToFour = 900     # Index 33
sixToFive = 470     # Index 35

fibreLimits[1] = oneToTwo
fibreLimits[3] = oneToFour
fibreLimits[8] = twoToThree
fibreLimits[6] = twoToOne
fibreLimits[11] = twoToSix
fibreLimits[13] = threeToTwo
fibreLimits[16] = threeToFive
fibreLimits[18] = fourToOne
fibreLimits[22] = fourToFive
fibreLimits[23] = fourToSix
fibreLimits[26] = fiveToThree
fibreLimits[27] = fiveToFour
fibreLimits[29] = fiveToSix
fibreLimits[31] = sixToTwo
fibreLimits[33] = sixToFour
fibreLimits[34] = sixToFive

# ------------------------------- #

droppedPackList = []
transferList =[]
fibreTracker = []

for count in range(36):
    l = []
    transferList.append(l)
for count in range(36):
    fibreTracker.append(0)

class node:
    def __init__(self,address,processTime,nodeSize,bufferSize,coreRoute,opOne,opTwo,opThree):
        self.address = address
        self.nodeSize = nodeSize
        self.processTime = processTime
        self.bufferSize = bufferSize
        self.packetList = []
        self.bufferList = []
        self.sentPackets = []
        self.coreRoute = coreRoute
        self.opOne = opOne
        self.opTwo = opTwo
        self.opThree = opThree
        self.packRec = 0
        self.packDrop = 0
        self.packBuff = 0

    def returnIterationData(self):
        print('RETURNING ITERATION DATA.')
        print('-------------------------')
        print('NODE ' + str(self.address) + ' TOTAL PACKETS RECIEVED: ' +str(self.packRec))
        print('NODE ' + str(self.address) + ' TOTAL PACKETS BUFFER: ' + str(self.packBuff))
        print('NODE ' + str(self.address) + ' TOTAL PACKETS DROPPED: ' +str(self.packDrop))
        print('-------------------------')

    def returnBufferList(self):
        return self.bufferList

    def processTime(self):
        time.sleep(self.processTime)

    def packetGen(self):
        # -- I HAD TO CHANGE THE CODE FOR PART NUMBER --
        # -- AS IT WAS THE PART INCLUDED A STRING SO COULDNT MATCH WHEN REQUESTING A RESEND
        # -- AGAIN, CODE CAN BE IMPLEMENTED TO KEEP TRACK OF HOW MANY PARTS A PACKET HAS.
        # -- EVENTUALLY WE WILL HAVE PACKETS CREATE A RANDOM AMOUNT OF PARTS FOR THEMSELVES.

        packetCount = 1000
        #packetCount = random.randint(1,self.nodeSize)
        returnCount = 0
        packetNo = 0
        print('CREATING ' + str(packetCount) + ' PACKETS FOR NODE ' + str(self.address))
        sentFrom = self.address
        while packetCount > 0:
            sendTo = random.randint(1,6)
            if sentFrom != sendTo:
                data = ''
                for count in range(3):
                    randNo = random.randint(0, 9)
                    data = data + str(randNo)
                packetNo += 1
                d = random.choice(dataType)
                for count in range(3):
                    timeStamp = time.time()
                    partNo = str(str(count+1))
                    p = packet(sentFrom, sendTo, data, d, timeStamp,partNo,packetNo)
                    self.packetList.append(p)
                    packetCount = packetCount - 1
                    returnCount += 1

        print('we created this many packets: ' + str(packetCount+returnCount))
        random.shuffle(self.packetList)
        return returnCount

    def returnRoutingPath(self,dest):
        possibleNodes = []
        for countOne in range(len(self.coreRoute)):
            if self.coreRoute[countOne] == dest:
                if self.opOne[countOne] != 0:
                    possibleNodes.append(self.opOne[countOne])
                if self.opTwo[countOne] != 0:
                    possibleNodes.append(self.opTwo[countOne])
                if self.opThree[countOne] != 0:
                    possibleNodes.append(self.opThree[countOne])

        return possibleNodes

    def sortPackets(self):

        global fibreTracker

        buffCount = self.checkBuffSize()
        if buffCount > 0:
            for count in range(len(self.bufferList)):
                self.packetList.append(self.bufferList[count])
            self.bufferList = []

        transferCount = 0
        packetsTransList = 0
        packetsTransBuff = 0
        packetsTransDrop = 0

        for count in range(len(self.packetList)):
            packet = self.packetList[count]
            dest = packet.returnDestination()
            index = (((self.address - 1) * numberOfNodes) + dest - 1)
            if fibreTracker[index] < fibreLimits[index]:
                transferList[index].append(packet)
                self.sentPackets.append(packet)
                fibreTracker[index] += 1
                packetsTransList += 1

            else:
                buffCount = self.checkBuffSize()
                if buffCount < self.bufferSize:
                    self.bufferList.append(self.packetList[count])
                    packetsTransBuff += 1
                else:
                    droppedPackList.append(self.packetList[count])
                    packetsTransDrop += 1

        for count in range(len(self.packetList)):
            self.removePacket()

        return transferCount

    def removePacket(self):
        if self.packetList == []:
            pass
        else:
            self.packetList.pop()

    def checkRemove(self,packetNo,sentFrom):
        delList = []
        delPack = 0
        length = len(self.packetList)

        for count in range(length):
            index = (length-count)-1
            packet = self.packetList[index]
            packNo = packet.returnPacketNo()
            packFrom = packet.returnSentFrom()
            if packNo == packetNo and packFrom == sentFrom:
                delList.append(index)

        for countTwo in range(len(delList)):
            del self.packetList[index]
            delPack += 1


    def checkPacketParts(self):

        checkingList =[]
        now = time.time()
        resendParts = 0

        for count in range(len(self.packetList)):
            packet = self.packetList[count]
            timeArrived = float(packet.returnTimeArrived())
            if int(abs(now-timeArrived)) > 2:
                checkingList.append(packet)

        for countTwo in range(len(checkingList)):
            if countTwo >= len(checkingList):
                break
            partList = []
            packet = checkingList[countTwo]
            partNo = packet.returnPartNo()
            packFrom = packet.returnSentFrom()
            packetNo = packet.returnPacketNo()
            partList.append(packet)
            for countThree in range(countTwo+1,len(checkingList)):
                packet2 = checkingList[countThree]
                packet2No = packet2.returnPacketNo()
                packet2Part = packet2.returnPartNo()
                pack2From = packet2.returnSentFrom()
                if packet2No == packetNo and pack2From == packFrom and packet2Part != partNo:
                    partList.append(packet2)
            fullPartPrint = []
            for x in range(len(partList)):
                fullPartPrint.append(partList[x].returnPartNo())
            if len(partList) == 3:
                packetsArrived.append(partList)
                packNo = partList[0].returnPacketNo()
                sentFrom = partList[0].returnSentFrom()
                self.checkRemove(packNo,sentFrom)
                for x in range(3):
                    checkingList.remove(partList[x])

            else:
                partCheckList = [1, 2, 3]
                partGotList = []
                sentFromNode = partList[0].returnSentFrom()
                packetNumber = partList[0].returnPacketNo()
                howMany = 3 - len(partList)
                if howMany == 1:
                    resendParts += 1
                else:
                    resendParts += 2

                for miniCount in range(len(partList)):
                    partNo = int(partList[miniCount].returnPartNo())
                    partGotList.append(partNo)

                mergedList = list(set(partGotList).symmetric_difference(set(partCheckList)))

                for x in range(len(partList)):
                    checkingList.remove(partList[x])

                for finalCount in range(len(mergedList)):
                    nodeList[sentFromNode].resendPart(packetNumber,mergedList[finalCount])

        for countThree in range(len(self.packetList)):
            packet = self.packetList[countThree]
            packet.resetTimeStamp()
            packet.recordTimeArrived(packet)

        print('HELLO, THIS IS NODE ' + str(self.address) + ' AND I HAVE REQUESTED A TOTAL OF ' + str(resendParts) + ' PACKETS TO BE RESENT FROM VARIOUS NODES.')

    def resendPart(self,packNo,partNo):
        for count in range(len(self.sentPackets)):
            packet = self.sentPackets[count]
            packetNo = int(packet.returnPacketNo())
            if packetNo == packNo:
                partNumber = int(packet.returnPartNo())
                if partNumber == partNo:
                    dest = packet.returnDestination()
                    possibleNodes = self.returnRoutingPath(dest)
                    randomNode = random.choice(possibleNodes)
                    if randomNode != 0:
                        nodeList[randomNode].recievePacket(packet)

    def recievePacket(self,packet):

        packet.addVisit(self.address)
        dest = packet.returnDestination()
        if self.address == dest:
            packet.recordTimeArrived(packet)
            nodeSize = self.checkListSize()
            buffSize = self.checkBuffSize()
            if nodeSize > self.nodeSize:
                if buffSize > self.bufferSize:
                    droppedPackList.append(packet)
                    self.packDrop += 1
                else:
                    self.bufferList.append(packet)
                    self.packBuff += 1
            else:
                self.packetList.append(packet)
                self.packRec += 1


    def checkListSize(self):
        return len(self.packetList)
    def checkBuffSize(self):
        return len(self.bufferList)

    def sendPackets(self):

        global transferList

        secondRange = (self.address-1)*numberOfNodes

        packetsMoved = 0
        if self.address == 1:
            for count in range(numberOfNodes):
                destList = transferList[count]
                for countTwo in range(len(destList)):
                    dest = destList[countTwo].returnDestination()
                    possibleNodes = self.returnRoutingPath(dest)
                    randomNode = random.choice(possibleNodes)
                    if randomNode != 0:
                        nodeList[randomNode].recievePacket(destList[countTwo])
                        packetsMoved += 1
        else:
            packMove = 0
            for count in range(numberOfNodes):
                destList = transferList[secondRange]
                secondRange += 1
                for countTwo in range(len(destList)):
                    dest = destList[countTwo].returnDestination()
                    if dest == self.address:
                        self.packetList.append(destList[countTwo])
                    else:
                        possibleNodes = self.returnRoutingPath(dest)
                        randomNode = random.choice(possibleNodes)
                        if randomNode != 0:
                            nodeList[randomNode].recievePacket(destList[countTwo])
                            packMove += 1

class packet:

    def __init__(self,sentFrom,sendTo,data,dataType,timeStamp,partNo,packetNo):
        self.sentFrom = sentFrom
        self.sendTo = sendTo
        self.data = data
        self.dataType = dataType
        self.timeStamp = timeStamp
        self.packetNo = packetNo
        self.partNo = partNo
        self.timeArrived = 0.0
        self.resetTime = 0.0
        self.visitedList = []

    def returnTimeArrived(self):
        return self.timeArrived

    def returnPacketNo(self):
        return self.packetNo

    def returnPartNo(self):
        return self.partNo

    def addVisit(self,nodeNumber):
        self.visitedList.append(nodeNumber)

    def returnVisitedList(self):
        return self.visitedList

    def resetTimeStamp(self):
        timeStamp = time.time()
        self.timeStamp = timeStamp


    def recordTimeArrived(self,packet):
        now = time.time()
        timeStamp = packet.returnTimeStamp()
        timeToArrival = str(now - timeStamp)
        self.timeArrived = timeToArrival

    def returnSentFrom(self):
        return self.sentFrom

    def returnDataType(self):
        return self.dataType

    def returnSendTo(self):
        return self.sendTo


    def returnDestination(self):
        return self.sendTo

    def returnTimeStamp(self):
        return self.timeStamp

    #def returnVisitedNodes(self):

    def returnPacketData(self):

        return self.data


def main():
    nodeZero = node(0,0,0,0,0,0,0,0)
    nodeList.append(nodeZero)
    nodeOne = node(1,0.2,500,1200,[2,3,4,5,6],[2,2,4,2,2],[0,4,0,4,4],[0,0,0,0,0])
    nodeList.append(nodeOne)
    nodeTwo = node(2,0.2,300,800,[1,3,4,5,6],[1,3,1,1,6],[0,0,3,3,0],[0,0,6,6,0])
    nodeList.append(nodeTwo)
    nodeThree = node(3,0.2,500,1100,[1,2,4,5,6],[2,2,2,5,2],[5,0,5,0,5],[0,0,0,0,0])
    nodeList.append(nodeThree)
    nodeFour = node(4,0.2,600,1500,[1,2,3,5,6],[1,1,1,5,6],[0,5,5,0,0],[0,6,6,0,0])
    nodeList.append(nodeFour)
    nodeFive = node(5,1,250,650,[1,2,3,4,6],[3,3,3,4,6],[4,4,0,0,0],[6,6,0,0,0])
    nodeList.append(nodeFive)
    nodeSix = node(6,0.2,550,1270,[1,2,3,4,5],[2,2,2,4,5],[4,0,4,0,0],[5,0,5,0,0])
    nodeList.append(nodeSix)
    nodeOneGen = nodeOne.packetGen()
    print(str(nodeOneGen) + ' packets generated in Node 1.')
    nodeTwoGen = nodeTwo.packetGen()
    print(str(nodeTwoGen) + ' packets generated in Node 2.')
    nodeThreeGen = nodeThree.packetGen()
    print(str(nodeThreeGen) + ' packets generated in Node 3.')
    nodeFourGen = nodeFour.packetGen()
    print(str(nodeFourGen) + ' packets generated in Node 4.')
    nodeFiveGen = nodeFive.packetGen()
    print(str(nodeFiveGen) + ' packets generated in Node 5.')
    nodeSixGen = nodeSix.packetGen()
    print(str(nodeSixGen) + ' packets generated in Node 6.')

    totalPack = nodeOneGen + nodeTwoGen + nodeThreeGen + nodeFourGen + nodeFiveGen + nodeSixGen

    # We now have a self.totalPacketArrived which will keep track of the packages that have reached their destination.

    print(' TOtal packages created : ' + str(totalPack))

    nodeOne.sortPackets()
    nodeOne.sendPackets()
    time.sleep(processTime[1])

    nodeTwo.sortPackets()
    nodeTwo.sendPackets()
    time.sleep(processTime[2])

    nodeThree.sortPackets()
    nodeThree.sendPackets()
    time.sleep(processTime[3])

    nodeFour.sortPackets()
    nodeFour.sendPackets()
    time.sleep(processTime[4])


    nodeFive.sortPackets()
    nodeFive.sendPackets()
    time.sleep(processTime[5])

    nodeSix.sortPackets()
    nodeSix.sendPackets()
    time.sleep(processTime[6])

    nodeOne.checkPacketParts()
    nodeTwo.checkPacketParts()
    nodeThree.checkPacketParts()
    nodeFour.checkPacketParts()
    nodeFive.checkPacketParts()
    nodeSix.checkPacketParts()


    print('-------------------------------------------')
    print('')

    #nodeOne.returnIterationData()
    #nodeTwo.returnIterationData()
    #nodeThree.returnIterationData()
    #nodeFour.returnIterationData()
    #nodeFive.returnIterationData()
    #nodeSix.returnIterationData()

    totalArrived = len(packetsArrived)

    print('TOTAL PACKETS ARRIVED AT DESTINATION: ' + str(totalArrived))
    
    ## Option block of packet information code ##
    
    #for count in range(len(packetsArrived)):
    #    print('---------------------------------------')
    #    print('')
    #    print('Packet arrival list index: ' + str(count))
    #    print('Packet data type: ' + str(packetsArrived[count].returnDataType()))
    #    print('Data from packet: ' + str(packetsArrived[count].returnPacketData()))
    #    print('Packet was sent from: ' + str(packetsArrived[count].returnSentFrom()))
    #    print('Packet was sent to: ' + str(packetsArrived[count].returnSendTo()))
    #    print('Routing path of packet: ' + str(packetsArrived[count].returnVisitedList()))
    #    print('This is packet number: ' + str(packetsArrived[count].returnPacketNo()))
    #    print('This was packet: ' + str(packetsArrived[count].returnPartNo()) + ' of packet number: ' + str(packetsArrived[count].returnPacketNo()))
    #    timeArrived = packetsArrived[count].returnTimeArrived()
    #    print('Package speed: ' + str(timeArrived) + ' seconds.' )
    #    print('')
    #    print('-----------------------------------------')

    print('')
    print('TOTAL PACKETS CREATED: ' + str(totalPack))
    print('TOTAL PACKETS ARRIVED: ' + str(totalArrived))
    print('-------------')

    nodeOneDest = []
    nodeTwoDest = []
    nodeThreeDest = []
    nodeFourDest = []
    nodeFiveDest = []
    nodeSixDest = []

    #for count in range(len(nodeOne.packetList)):
    #    dest = str(nodeOne.packetList[count].returnDestination())
    #    nodeOneDest.append(dest)
    #print('ALL NODE ONE DESTINATIONS: ' + str(nodeOneDest))
    #for count in range(len(nodeTwo.packetList)):
    #    dest = str(nodeTwo.packetList[count].returnDestination())
    #    nodeTwoDest.append(dest)
    #print('NODE TWO DESTINATIONS: ' + str(nodeTwoDest))
    #for count in range(len(nodeThree.packetList)):
    #    dest = str(nodeThree.packetList[count].returnDestination())
    #    nodeThreeDest.append(dest)
    #print('NODE THREE DESTINATIONS: ' + str(nodeThreeDest))
    #for count in range(len(nodeFour.packetList)):
    #    dest = str(nodeFour.packetList[count].returnDestination())
    #    nodeFourDest.append(dest)
    #print('NODE FOUR DESTINATIONS: ' + str(nodeFourDest))
    #for count in range(len(nodeFive.packetList)):
    #    dest = str(nodeFive.packetList[count].returnDestination())
    #    nodeFiveDest.append(dest)
    #print('NODE FIVE DESTINATIONS: ' + str(nodeFiveDest))
    #for count in range(len(nodeSix.packetList)):
    #    dest = str(nodeSix.packetList[count].returnDestination())
    #    nodeSixDest.append(dest)
    #print('NODE SIX DESTINATIONS: ' + str(nodeSixDest))

    print('---------------------------')
    print('PACKAGES LEFT IN NODE ONE: ' + str(len(nodeOne.packetList)))
    print('--------------------------')
    print('PACKAGES LEFT IN NODE TWO: ' + str(len(nodeTwo.packetList)))
    print('--------------------------')
    print('PACKAGES LEFT IN NODE THREE: ' + str(len(nodeThree.packetList)))
    print('--------------------------')
    print('PACKAGES LEFT IN NODE FOUR: ' + str(len(nodeFour.packetList)))
    print('--------------------------')
    print('PACKAGES LEFT IN NODE FIVE: ' + str(len(nodeFive.packetList)))
    print('--------------------------')
    print('PACKAGES LEFT IN NODE SIX: ' + str(len(nodeSix.packetList)))

    nodeOneBuff = nodeOne.returnBufferList()
    nodeTwoBuff = nodeTwo.returnBufferList()
    nodeThreeBuff = nodeThree.returnBufferList()
    nodeFourBuff = nodeFour.returnBufferList()
    nodeFiveBuff = nodeFive.returnBufferList()
    nodeSixBuff = nodeSix.returnBufferList()

    print('TOTAL LEFT IN BUFFER ONE: ' + str(len(nodeOneBuff)))
    print('TOTAL LEFT IN BUFFER TWO: ' + str(len(nodeTwoBuff)))
    print('TOTAL LEFT IN BUFFER THREE: ' + str(len(nodeThreeBuff)))
    print('TOTAL LEFT IN BUFFER FOUR: ' + str(len(nodeFourBuff)))
    print('TOTAL LEFT IN BUFFER FIVE: ' + str(len(nodeFiveBuff)))
    print('TOTAL LEFT IN BUFFER SIX: ' + str(len(nodeSixBuff)))
    print('SIZE OF DROPPED PACKET LIST: ' + str(len(droppedPackList)))

    print(fibreLimits[::])
    print(fibreTracker[::])


    # THE FOLLOWING PRINT STATEMENTS SHOW THAT EVERY PACKET'S DESTINATION DOES NOT MATCH ITS CURRENT CODE PACKET LIST.


main()
