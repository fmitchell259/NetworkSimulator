import random, time, collections

resentParts = []
nodeList = []
dataType = ['Video', 'Textfile', 'Audio', 'Code', 'Image', 'Game Streaming', 'Download Data','Audio Streaming','Video Streaming']
packetsArrived = []
numberOfNodes = 6
processTime = [0, 0.2, 0.2, 0.2, 0.2, 1, 0.2]

## Fibre Link Limitations ##

fibreLimits = []

for count in range(36):
    fibreLimits.append(0)

routingDictList = []

for count in range(36):
    dictList = {}
    routingDictList.append(dictList)


oneToTwo = 400  # Index 1
oneToFour = 600  # Index 2
twoToThree = 550  # Index 8
twoToOne = 400  # Index 6
twoToSix = 270  # Index 10
threeToTwo = 500  # Index 13
threeToFive = 450  # Index 16
fourToOne = 600  # Index 18
fourToFive = 800  # Index 22
fourToSix = 900  # Index 23
fiveToThree = 450  # Index 26
fiveToFour = 800  # Index 27
fiveToSix = 470  # Index 29
sixToTwo = 270  # Index 31dropped
sixToFour = 900  # Index 33
sixToFive = 470  # Index 35

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
transferList = []
fibreTracker = []
timeTrackerList = []

for count in range(36):
    l = []
    transferList.append(l)
for count in range(36):
    fibreTracker.append(0)

# Creating new lists to track best routes.

for count in range(36):
    bestTimeList = []
    timeTrackerList.append(bestTimeList)


def findBestTimes(arrivedList):

    for count2 in range(len(arrivedList)):
        packetList = arrivedList[count2]
        packet = packetList[0]
        packFrom = packet.returnSentFrom()
        if packFrom == 1:
            packDest = packet.returnDestination()
            index = packDest - 1
            timeTrackerList[index].append(packet)
        else:
            packDest = packet.returnDestination()
            index = ((packFrom - 1)*6) + (packDest-1)
            timeTrackerList[index].append(packet)


    for count4 in range(len(timeTrackerList)):
        list = timeTrackerList[count4]
        if list == []:
            pass
        while len(list) > 10:
            packet1 = list[0]
            packet1Time = packet1.returnTimeArrived()
            packet2 = list[1]
            packet2Time = packet2.returnTimeArrived()
            if packet1Time < packet2Time:
                list.pop(1)
            elif packet1Time > packet2Time:
                list.pop(2)
            elif packet1Time == packet2Time:
                pack1Route = packet1.visitedList
                pack2Route = packet2.visitedList
                if pack1Route == pack2Route:
                    list.pop(1)


class node:
    def __init__(self, address, processTime, nodeSize, bufferSize, coreRoute, opOne, opTwo, opThree):
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
        self.forwardList = []

    def returnIterationData(self):
        print('RETURNING ITERATION DATA.')
        print('-------------------------')
        print('NODE ' + str(self.address) + ' TOTAL PACKETS RECIEVED: ' + str(self.packRec))
        print('NODE ' + str(self.address) + ' TOTAL PACKETS BUFFER: ' + str(self.packBuff))
        print('NODE ' + str(self.address) + ' TOTAL PACKETS DROPPED: ' + str(self.packDrop))
        print('-------------------------')

    def returnBufferList(self):
        return self.bufferList

    def processTime(self):
        time.sleep(self.processTime)

    def packetGen(self):
        packetCount = 1000
        returnCount = 0
        packetNo = 0
        print('CREATING ' + str(packetCount) + ' PACKETS FOR NODE ' + str(self.address))
        sentFrom = self.address
        while packetCount > 0:
            sendTo = random.randint(1, 6)
            if sentFrom != sendTo:
                data = ''
                for count in range(3):
                    randNo = random.randint(0, 9)
                    data = data + str(randNo)
                packetNo += 1
                d = random.choice(dataType)
                for count in range(3):
                    timeStamp = time.time()
                    partNo = str(str(count + 1))
                    p = packet(sentFrom, sendTo, data, d, timeStamp, partNo, packetNo)
                    self.forwardList.append(p)
                    packetCount = packetCount - 1
                    returnCount += 1

        print('We created this many packets: ' + str(packetCount + returnCount))
        random.shuffle(self.packetList)
        return returnCount

    def returnRoutingPath(self, dest):
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
                self.forwardList.append(self.bufferList[count])
            self.bufferList = []

        transferCount = 0
        packetsTransList = 0
        packetsTransBuff = 0
        packetsTransDrop = 0

        if self.address == 1:
            for count in range(len(self.forwardList)):
                packet = self.forwardList[count]
                dest = packet.returnDestination()
                possibleNodes = self.returnRoutingPath(dest)
                randomNode = 0
                while randomNode == 0:
                    randomNode = random.choice(possibleNodes)
                    if randomNode != 0:
                        index = randomNode -1
                        if fibreTracker[index] < fibreLimits[index]:
                            fibreTracker[index] += 1
                            transferList[index].append(packet)
                            self.sentPackets.append(packet)
                            packetsTransList += 1
                        else:
                            buffCount = self.checkBuffSize()
                            if buffCount < self.bufferSize:
                                self.bufferList.append(self.forwardList[count])
                                packetsTransBuff += 1
                            else:
                                droppedPackList.append(self.forwardList[count])
                                packetsTransDrop += 1
        else:
            for count in range(len(self.forwardList)):
                packet = self.forwardList[count]
                dest = packet.returnDestination()
                possibleNodes = self.returnRoutingPath(dest)
                randomNode = 0
                while randomNode == 0:
                    randomNode = random.choice(possibleNodes)
                    if randomNode != 0:
                        index = ((self.address - 1) * numberOfNodes) + (randomNode-1)
                        if fibreTracker[index] < fibreLimits[index]:
                            fibreTracker[index] += 1
                            transferList[index].append(packet)
                            self.sentPackets.append(packet)
                            packetsTransList += 1
                        else:
                            buffCount = self.checkBuffSize()
                            if buffCount < self.bufferSize:
                                self.bufferList.append(self.forwardList[count])
                                packetsTransBuff += 1
                            else:
                                droppedPackList.append(self.forwardList[count])
                                packetsTransDrop += 1
        self.forwardList = []

        return transferCount

    def removePacket(self):
        if self.packetList == []:
            pass
        else:
            self.packetList.pop()

    def checkRemove(self, packetNo, sentFrom):
        delList = []
        delPack = 0
        length = len(self.packetList)

        for count in range(length):
            index = (length - count) - 1
            packet = self.packetList[index]
            packNo = packet.returnPacketNo()
            packFrom = packet.returnSentFrom()
            if packNo == packetNo and packFrom == sentFrom:
                delList.append(index)



        for countTwo in range(len(delList)):
            del self.packetList[delList[countTwo]]
            delPack += 1



    def checkPacketParts(self):

        checkingList = []
        now = time.time()
        resendParts = 0
        streamedPartsRemoved = 0

        for count in range(len(self.packetList)):
            packet = self.packetList[count]
            if abs(now - packet.timeStamp) > 2.0:
                checkingList.append(packet)

        checkLength = len(checkingList)


        while checkLength > 0:
                partList = []
                packet = checkingList[0]
                partNo = packet.returnPartNo()
                packFrom = packet.returnSentFrom()
                packetNo = packet.returnPacketNo()
                partList.append(packet)
                for countThree in range(1, checkLength):
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
                    for y in range(len(partList)):
                        packetDel = partList[y]
                        packDelNo = packetDel.returnPacketNo()
                        packDelFrom = packetDel.returnSentFrom()
                        self.checkRemove(packDelNo, packDelFrom)
                    for x in range(3):
                        checkingList.remove(partList[x])

                    checkLength = len(checkingList)

                else:

                    streamCheckPack = partList[0]
                    streamCheckData = streamCheckPack.returnDataType()
                    if 'Stream' in streamCheckData:
                        for count9 in range(len(partList)):
                            packet = partList[count9]
                            checkListIndex = checkingList.index(packet)
                            if packet in self.packetList:
                                packetListIndex = self.packetList.index(packet)
                                checkingList.pop(checkListIndex)
                                droppedPackList.append(packet)
                                self.packetList.pop(packetListIndex)
                                streamedPartsRemoved += 1
                            else:
                                droppedPackList.append(packet)
                                streamedPartsRemoved += 1
                                pass

                        checkLength = len(checkingList)

                    else:
                        partCheckList = [1, 2, 3]
                        partGotList = []
                        sentFromNode = partList[0].returnSentFrom()
                        packetNumber = partList[0].returnPacketNo()


                        for miniCount in range(len(partList)):
                            partNo = int(partList[miniCount].returnPartNo())
                            partGotList.append(partNo)

                        mergedList = list(set(partGotList).symmetric_difference(set(partCheckList)))


                        howMany = 3 - len(mergedList)

                        if howMany == 1:
                            resendParts += 1
                            #print('ADDED ONE TO HOW MANY')
                        elif howMany == 2:
                            resendParts += 2
                            #print('ADDED two TO HOW MANY')

                        for x in range(len(partList)):
                            checkingList.remove(partList[x])

                        checkLength = len(checkingList)

                        for finalCount in range(len(mergedList)):
                            nodeList[sentFromNode].resendPart(packet,packetNumber, mergedList[finalCount])

        for countThree in range(len(self.packetList)):
            packet = self.packetList[countThree]
            packet.resetTimeStamp()
            packet.recordTimeArrived()
        print('THIS IS NODE: ' + str(self.address) + " REMOVED THIS MANY STREAM PACKETS: " + str(streamedPartsRemoved))

    def resendPart(self,packet, packNo, partNo):


        for count in range(len(self.sentPackets)):
            packet = self.sentPackets[count]
            packetNo = int(packet.returnPacketNo())
            if packetNo == packNo:
                partNumber = int(packet.returnPartNo())

                if partNumber == partNo:
                    dest = packet.returnDestination()
                    possibleNodes = self.returnRoutingPath(dest)
                    randomNode = 0
                    while randomNode == 0:
                        randomNode = random.choice(possibleNodes)
                        if randomNode != 0:
                            packet.resent = True
                            nodeList[randomNode].recievePacket(packet)
                            resentParts.append(packet)




        for count4 in range(len(self.sentPackets)):
            packetDel = self.sentPackets[count4]
            if packet == packetDel:
                self.sentPackets.remove(packetDel)


    def recievePacket(self, packet):


        packet.addVisit(self.address)
        dest = packet.returnDestination()
        if self.address == dest:
            packet.recordTimeArrived()
            self.packetList.append(packet)
            self.packRec += 1
        else:
            self.forwardList.append(packet)


    def checkListSize(self):
        return len(self.packetList)

    def checkBuffSize(self):
        return len(self.bufferList)

    def sendPackets(self):

        global transferList

        secondRange = (self.address - 1) * numberOfNodes

        packetsMoved = 0
        if self.address == 1:
            for count in range(numberOfNodes):
                destList = transferList[count]
                destNode = count + 1
                for countTwo in range(len(destList)):
                    nodeList[destNode].recievePacket(destList[countTwo])
                    packetsMoved += 1
        else:
            for count in range(numberOfNodes):
                destList = transferList[secondRange+count]
                destNode = count + 1
                for countTwo in range(len(destList)):
                    nodeList[destNode].recievePacket(destList[countTwo])
                    packetsMoved += 1

        for count3 in range(len(transferList)):
            list = transferList[count3]
            list = []

class packet:

    def __init__(self, sentFrom, sendTo, data, dataType, timeStamp, partNo, packetNo):
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
        self.resent = False

    def returnTimeArrived(self):
        return self.timeArrived

    def returnPacketNo(self):
        return self.packetNo

    def returnPartNo(self):
        return self.partNo

    def addVisit(self, nodeNumber):
        self.visitedList.append(nodeNumber)

    def returnVisitedList(self):
        return self.visitedList

    def resetTimeStamp(self):
        timeStamp = time.time()
        self.timeStamp = timeStamp

    def recordTimeArrived(self):
        now = time.time()
        self.timeArrived = now

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

    # def returnVisitedNodes(self):

    def returnPacketData(self):
        return self.data

def emptyResent():
     global resentParts
     resentParts = []

def main():
    nodeZero = node(0, 0, 0, 0, 0, 0, 0, 0)
    nodeList.append(nodeZero)
    nodeOne = node(1, 0.2, 1010, 1200, [2, 3, 4, 5, 6], [2, 2, 4, 2, 2], [0, 4, 0, 4, 4], [0, 0, 0, 0, 0])
    nodeList.append(nodeOne)
    nodeTwo = node(2, 0.2, 1010, 800, [1, 3, 4, 5, 6], [1, 3, 1, 1, 6], [0, 0, 3, 3, 0], [0, 0, 6, 6, 0])
    nodeList.append(nodeTwo)
    nodeThree = node(3, 0.2, 1010, 1100, [1, 2, 4, 5, 6], [2, 2, 2, 5, 2], [5, 0, 5, 0, 5], [0, 0, 0, 0, 0])
    nodeList.append(nodeThree)
    nodeFour = node(4, 0.2, 1010, 1500, [1, 2, 3, 5, 6], [1, 1, 1, 5, 6], [0, 5, 5, 0, 0], [0, 6, 6, 0, 0])
    nodeList.append(nodeFour)
    nodeFive = node(5, 1, 1010, 650, [1, 2, 3, 4, 6], [3, 3, 3, 4, 6], [4, 4, 0, 0, 0], [6, 6, 0, 0, 0])
    nodeList.append(nodeFive)
    nodeSix = node(6, 0.2, 1010, 1270, [1, 2, 3, 4, 5], [2, 2, 2, 4, 5], [4, 0, 4, 0, 0], [5, 0, 5, 0, 0])
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

    totalArrived = len(packetsArrived)

    print('TOTAL PACKETS ARRIVED AT DESTINATION: ' + str(totalArrived))

    print('')
    print('TOTAL PACKETS CREATED: ' + str(totalPack))
    print('TOTAL PACKETS ARRIVED: ' + str(totalArrived))
    print('-------------')
    print('---------------------------')
    print('PACKAGES LEFT IN NODE ONE FORWARD LIST: ' + str(len(nodeOne.forwardList)))
    print('--------------------------')
    print('PACKAGES LEFT IN NODE TWO FORWARD LIST: ' + str(len(nodeTwo.forwardList)))
    print('--------------------------')
    print('PACKAGES LEFT IN NODE THREE FORWARD LIST: ' + str(len(nodeThree.forwardList)))
    print('--------------------------')
    print('PACKAGES LEFT IN NODE FOUR FORWARD LIST: ' + str(len(nodeFour.forwardList)))
    print('--------------------------')
    print('PACKAGES LEFT IN NODE FIVE FORWARD LIST: ' + str(len(nodeFive.forwardList)))
    print('--------------------------')
    print('PACKAGES LEFT IN NODE SIX FORWARD LIST: ' + str(len(nodeSix.forwardList)))

    nodeOneBuff = nodeOne.returnBufferList()
    nodeTwoBuff = nodeTwo.returnBufferList()
    nodeThreeBuff = nodeThree.returnBufferList()
    nodeFourBuff = nodeFour.returnBufferList()
    nodeFiveBuff = nodeFive.returnBufferList()
    nodeSixBuff = nodeSix.returnBufferList()

    print('------------------------------')
    print('TOTAL LEFT IN BUFFER ONE: ' + str(len(nodeOneBuff)))
    print('TOTAL LEFT IN BUFFER TWO: ' + str(len(nodeTwoBuff)))
    print('TOTAL LEFT IN BUFFER THREE: ' + str(len(nodeThreeBuff)))
    print('TOTAL LEFT IN BUFFER FOUR: ' + str(len(nodeFourBuff)))
    print('TOTAL LEFT IN BUFFER FIVE: ' + str(len(nodeFiveBuff)))
    print('TOTAL LEFT IN BUFFER SIX: ' + str(len(nodeSixBuff)))
    print('')
    print('--------------------------------')
    print('SIZE OF DROPPED PACKET LIST: ' + str(len(droppedPackList)))
    print('--------------------------------')

    print('FIBRE LIMIT LIST: ' + '\t' + str(fibreLimits[::]))
    print('FIBRE TRACKER LIST: ' + str(fibreTracker[::]))

    print('---------------------------')
    print('PACKAGES LEFT IN NODE ONE PACKET LIST: ' + str(len(nodeOne.packetList)))
    print('--------------------------')
    print('PACKAGES LEFT IN NODE TWO PACKET LIST: ' + str(len(nodeTwo.packetList)))
    print('--------------------------')
    print('PACKAGES LEFT IN NODE THREE PACKET LIST: ' + str(len(nodeThree.packetList)))
    print('--------------------------')
    print('PACKAGES LEFT IN NODE FOUR PACKET LIST: ' + str(len(nodeFour.packetList)))
    print('--------------------------')
    print('PACKAGES LEFT IN NODE FIVE PACKET LIST: ' + str(len(nodeFive.packetList)))
    print('--------------------------')
    print('PACKAGES LEFT IN NODE SIX PACKET LIST: ' + str(len(nodeSix.packetList)))

    print('============================')
    print('--------------------------')
    print('---------------------------')
    print('')
    print('Total Number of resent Packets: ' + str(len(resentParts)))
    print('')

    emptyResent()

    findBestTimes(packetsArrived)

    listOrdered = []
    for count11 in range(36):
        list = []
        listOrdered.append(list)

    print('')
    print('Franks Network best route finder.')
    print('=================================')
    print('')
    print('Below is a list of 36 tuples that have been created from an ordered dicionary.')
    print('I added the 10 fastest routes and their respective next nodes to the dictionary that became this list of tuples.')
    print('This solution did find the fastest routes per journey and very quick to code but the output is messy and it takes')
    print('a very long time to load.')
    print('')

    for count9 in range(len(timeTrackerList)):
        list = timeTrackerList[count9]
        for count10 in range(len(list)):
            packet = list[count10]
            packArr = packet.returnTimeArrived()
            packCreate = packet.returnTimeStamp()
            time2arrive = packArr - packCreate
            firstNode = packet.visitedList[0]
            routingDictList[count9].update({time2arrive:firstNode})

        dict = routingDictList[count9]
        ordDic = collections.OrderedDict(sorted(dict.items()))
        listOrdered[count9] = ordDic

        print(ordDic)

    # THE FOLLOWING PRINT STATEMENTS SHOW THAT EVERY PACKET'S DESTINATION DOES NOT MATCH ITS CURRENT CODE PACKET LIST.


main()
