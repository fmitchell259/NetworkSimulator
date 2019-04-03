import random, time, collections

# Initialise the lists I need for each
# of my functions (creating packets, sending
# packets, counting packets etc..)

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

# These variables represent the amount of
# packets that can go down a particular fibre link.

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
sixToTwo = 270  # Index 31
sixToFour = 900  # Index 33
sixToFive = 470  # Index 35

# The figures are then added to each list within
# the containing fibreTrackerList.

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

# Create another list of lists to find best times.

for count in range(36):
    bestTimeList = []
    timeTrackerList.append(bestTimeList)

def topThree():

    # Start by creating two empty lists which will also hold a bunch of lists.
    # The lists within nodetracker and bestTimeTracker will correspond to journeys through the network.

    nodeTracker = []
    bestTimeTracker = []


    for counting in range(36):
        nodeList = []
        timeList = []
        nodeTracker.append(nodeList)
        bestTimeTracker.append(timeList)

    # Fill up my list of lists with [0,0,0] and [999,999,999].
    # This gives me something to compare when iterating over my bestTimeTracker list.

    for count13 in range(36):
        nodeL = nodeTracker[count13]
        timeList = bestTimeTracker[count13]
        nodeL.append(0)
        nodeL.append(0)
        nodeL.append(0)
        timeList.append(999)
        timeList.append(999)
        timeList.append(999)


    for count11 in range(len(timeTrackerList)):

        # Go through timeTracker and pick up a journey list.
        # Pick up the appropriate bestNode and bestTime list (i.e. journey 1-2, 1-3, 1-4 etc.)

        journeyList = timeTrackerList[count11]
        bestNodeList = nodeTracker[count11]
        bestTime = bestTimeTracker[count11]

        for count12 in range(len(journeyList)):

            # Go through each journeyList and pick up a packet.
            # Check where it came from, where it is going and the time it took to get there.
            # This info all used to compare with our bestTime and bestNode list.

            packetCheck = journeyList[count12]
            packArr = packetCheck.returnTimeArrived()
            packCreate = packetCheck.returnTimeStamp()
            bestNode = packetCheck.visitedList[0]
            timeArr = packArr - packCreate


            if timeArr < bestTime[2] and timeArr < bestTime[1] and timeArr > bestTime[0]:

                # Save my best time and nodes in index 2.

                time = bestTime[1]
                node = bestNodeList[1]

                # Shift  the best time along and set my new best time in index 2.

                bestTime[2] = time
                bestTime[1] = timeArr

                # Set my new best node and set my new best node in index 2.

                bestNodeList[2] = node
                bestNodeList[1] = bestNode

            if timeArr < bestTime[2] and timeArr < bestTime[1] and timeArr < bestTime[0]:

                # Save my two best times from index 0 and index 1

                time0 = bestTime[0]
                time1 = bestTime[1]

                # Save my two best nodes from index 0 and index 1.

                node0 = bestNodeList[0]
                node1 = bestNodeList[1]

                # Shift my times along by one index and put new best time in index 0.

                bestTime[1] = time0
                bestTime[2] = time1
                bestTime[0] = timeArr

                # Shift my nodes along by one index and put new best time in index 0.

                bestNodeList[1] = node0
                bestNodeList[2] = node1
                bestNodeList[0] = bestNode

            if timeArr < bestTime[2] and timeArr > bestTime[1]:

                # No need to save the times or nodes from other indexes, just replace the last item in both lists with the best time and node.

                bestTime[2] = timeArr
                bestNodeList[2] = bestNode

    # Using python's built in zip function we pull our two lists together to output a tuple.
    # Each tuple represents a journey (1-2,1-3,1-4 etc) with the top three (from left to right) in each tuple.

    finalBestList = list(zip(nodeTracker,bestTimeTracker))

    for count21 in range(len(finalBestList)):
        journey = finalBestList[count21]
        print('Journey: ' + str(count21+1) + ' : ' + str(journey))


def findBestTimes(arrivedList):

    # This function DOES NOT fund the best times.
    # it simply sorts the packets into the
    # timeTracker list of lists ready for the function
    # topThree to find the BEST times.

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

        # Create 1000 packets, made up of 3 sub-packets
        # for each node.

        packetCount = 1000
        # packetCount = random.randint(1,self.nodeSize)
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

        print('we created this many packets: ' + str(packetCount + returnCount))
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

        # Import my global fibreTracker list, this list limits
        # the amount of packets that can go down a fibre link.

        # Also import global transferList, this a list of lists
        # representing journey's 1-2, 1-3, 1-4 etc..

        global fibreTracker
        global transferList

        # Before doing anything a node checks its buffer and brings
        # packets from there into its buffer list.

        buffCount = self.checkBuffSize()
        if buffCount > 0:
            for count in range(len(self.bufferList)):
                self.forwardList.append(self.bufferList[count])
            self.bufferList = []

        # Set all counters to zer to keep track of what is going where.

        transferCount = 0
        packetsTransList = 0
        packetsTransBuff = 0
        packetsTransDrop = 0

        # My sorting algorithm works in two ways. Because my transferList
        # is a list of lists, I needed a wee bit of maths to pick up the
        # correct list. This works one way when the address is 1 and a
        # slightly different way when the address is greater than 1.

        # The following block sorts packets from a node's forwardList and
        # puts them in their appropriate transferList list. This is depending
        # on the nodes routing table, the size of the fibreLimit, and
        # the size of the buffer.

        # We also create a copy of all the packets sent to allow other nodes
        # to request a re-send if a packet has not arrived.

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

        # As mentioned above, the same code block is repeated when the address
        # is greater than 1.

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

        # Empty the forwardList, ready for the next iteration of packets.

        self.forwardList = []

        # Return total packets transferred out of node.

        return transferCount

    def removePacket(self):

        if self.packetList == []:
            pass
        else:
            self.packetList.pop()

    def checkRemove(self, packetNo, sentFrom):

        # A small function to remove packets
        # from a node's packetList.

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

        # Create a checkingList, this will be populated by
        # packets that have been waiting longer than 2 seconds.

        checkingList = []
        now = time.time()
        resendParts = 0
        streamedPartsRemoved = 0

        # Check if a packet in a nodes packetList has been waiting longer
        # then two seconds, if so, add it to checkingList.

        for count in range(len(self.packetList)):
            packet = self.packetList[count]
            if abs(now - packet.timeStamp) > 2.0:
                checkingList.append(packet)

        # Set my control variable checkLength, this will be used
        # to check each packet in the checkingList has every part.

        checkLength = len(checkingList)


        # Iterate over checkingList until all packets have beeb checked
        # for all parts.

        # We put each packet in a partList and then check for all three
        # parts. If we find all three the partList containing all three
        # of our packet parts is added to global packetsArrived list.

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

                if len(partList) == 3:
                    packetsArrived.append(partList)
                    for y in range(len(partList)):
                        packetDel = partList[y]
                        packDelNo = packetDel.returnPacketNo()
                        packDelFrom = packetDel.returnSentFrom()
                        self.checkRemove(packDelNo, packDelFrom)
                    for x in range(3):
                        checkingList.remove(partList[x])

                    # Always adjust checkLength when removing packets.

                    checkLength = len(checkingList)

                else:

                    # If we don't have all three parts then we need to
                    # first check if the packet is sa 'Streaming' packet.

                    # If the packet is not a streaming packet we must
                    # request a re-send.

                    # Pick up one of the parts of the packet in partList.
                    # Check if this packet has 'Stream' in it's data-type.

                    streamCheckPack = partList[0]
                    streamCheckData = streamCheckPack.returnDataType()

                    # If we find the word 'Stream' then remove that part.
                    # Also remove this packet from the packetList.
                    # Streaming packets are lossy data and as such can be dropped


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

                        # Once 'Stream' packets have been removed we need to
                        # re-assess checkLength, this variable is the control
                        # within the while loop.

                        checkLength = len(checkingList)

                    # If the packet is not a 'Streaming' packet we then
                    # request a re-send. This is done by comparing with my
                    # partCheckList which contains [1,2,3].

                    else:
                        partCheckList = [1, 2, 3]
                        partGotList = []
                        sentFromNode = partList[0].returnSentFrom()
                        packetNumber = partList[0].returnPacketNo()


                        # The partList contains packet objects so a loop is required
                        # to produce a partGotList of each packet's part number.

                        for miniCount in range(len(partList)):
                            partNo = int(partList[miniCount].returnPartNo())
                            partGotList.append(partNo)


                        # Using 'symemetric_difference' and 'set' we can then produce a
                        # final list of the parts we need to request from various nodes.

                        # This is mergingo my checkPartParts and my partGotList, to give
                        # me mergedList, showing the differences between the two. i.e
                        # the parts I need to re-request.

                        mergedList = list(set(partGotList).symmetric_difference(set(partCheckList)))

                        # The following just allows me to count how many packets
                        # are being re-sent.

                        howMany = 3 - len(mergedList)

                        if howMany == 1:
                            resendParts += 1
                        elif howMany == 2:
                            resendParts += 2

                        # Go over my checking list and remove the packets
                        # I havein the partList.

                        for x in range(len(partList)):
                            checkingList.remove(partList[x])

                        # Always adjust my control variable (checkLength) when removing
                        # packets from the checkingList.

                        checkLength = len(checkingList)

                        # Finally request a re-send of one or two parts of a packet.

                        for finalCount in range(len(mergedList)):
                             nodeList[sentFromNode].resendPart(packet,packetNumber, mergedList[finalCount])


        # Lastly we need to reset the timeStamp on the packets
        # waiting for a re-send to arrive.

        for countThree in range(len(self.packetList)):
            packet = self.packetList[countThree]
            packet.resetTimeStamp()
            packet.recordTimeArrived()
        print('THIS IS NODE: ' + str(self.address) + " REMOVED THIS MANY STREAM PACKETS: " + str(streamedPartsRemoved))

    def resendPart(self,packet, packNo, partNo):

        # Iterate over a nodes sentPackets list and
        # find the missing packet. Consult that nodes
        # routing table and re-send.

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

        # Once a re-send has been completed, delete that packet
        # from the sentPackets list.

        for count4 in range(len(self.sentPackets)):
            packetDel = self.sentPackets[count4]
            if packet == packetDel:
                self.sentPackets.remove(packetDel)


    def recievePacket(self, packet):

        # As soon as a packet is received we add that
        # node to the packets visitedList. This lets us
        # keep track of which nodes a packet has visited.

        packet.addVisit(self.address)

        # Work out where this packet is destined for?

        dest = packet.returnDestination()

        # If the packet has noe arrived, record its time
        # of arrival and add to that nodes packetList.

        # If the packet still needs to continue on its
        # journey put the packet in that nodes forwardList.

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

        # Import my transferList. This is my list of lists
        # representing the journey's through the network.
        # After a node has sorted its packets these lists are all
        # full of packets ready to be sent to their respective nodes.

        global transferList

        # This secondRange is the small piece of maths I have
        # used to pick up the right list of lists index. This
        # only needs to be used when the address is greater than 1.

        secondRange = (self.address - 1) * numberOfNodes

        packetsMoved = 0

        # Iterate over trasnferList, pick up a journey list
        # and send the packets on their way.

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

        # Clear all my lists for the next iteration.

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

    # Below are a series of small functions
    # that return various information about a packet.

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

    def returnPacketData(self):
        return self.data

def emptyResent():

    # I have a global resent list to keep track
    # of how may packets get resent, by each node,
    # per iteration.

    # This list needs to emptied before the next
    # iteration.

     global resentParts

     resentParts = []

def main():

    # Import global nodeList.
    # This allows me to access all the methods associated with any particular node from anywhere within the system.

    global nodeList

    # Create my six nodes.
    # Node zero is created and never used to allow for consistent numbers.

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

    # Create packets within each node.
    # A node cannot create a packet destined for itself.
    # Print statements to allow developer to track packets.

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
    print(' TOtal packages created : ' + str(totalPack))

    # Start the process of sending packets.
    # Each node sorts the packets in their packetList
    # The packets get transferred to a global transferList, sorted into journey (1-2, 3-5, 4-2 etc...).
    # Packets are then taken from each respective journey list and sent to their respective nodes.
    # The sleep function aims to imitate the time for a node to process the data.

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

    # When all packets have been sorted and sent they are held in a nodes checkingList.
    # This allows for a node to check that all 'parts' of a packet have been received.
    # If a packet has been waiting longer than 2 seconds it will be checked for completeness.
    # If a packet is complete it will be removed from the node completely and added to the global packetsArrived list.
    # Items in this list comprise a list of three 'parts' of a packet (which are packet objects themselves).

    nodeOne.checkPacketParts()
    nodeTwo.checkPacketParts()
    nodeThree.checkPacketParts()
    nodeFour.checkPacketParts()
    nodeFive.checkPacketParts()
    nodeSix.checkPacketParts()

    # The following print statements and method calls allow the developer to ensure
    # their are no missing packets, or duplicate packets, within the system.

    # The total packets in a nodes packetList, bufferlist and any packets dropped should
    # be equal to the total packets created plus the number of packets re-requested.


    print('-------------------------------------------\n')

    totalArrived = len(packetsArrived)

    print('TOTAL PACKETS ARRIVED AT DESTINATION: ' + str(totalArrived) + '\n')
    print('TOTAL PACKETS CREATED: ' + str(totalPack))
    print('TOTAL PACKETS ARRIVED: ' + str(totalArrived))
    print('-------------\n')
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
    print('--------------------------\n')
    print('Total Number of resent Packets: ' + str(len(resentParts)) + '\n')

    # After each iteration I need to empty the list that collects each resent part.
    # This global list is used to count the number of packets a node resends.

    # After one iteration I need to reset this list to keep count of the total packets
    # resent with multiple iterations.

    emptyResent()

    # The function findBestTimes gets packets out of the packetsArrived list and
    # puts them into my timeTracker list of lists (a list of journeys).

    findBestTimes(packetsArrived)

    # The function topThree iterates over each sorted timeTracker packet and creates
    # a top three fastest packets for each journey in the network.

    # A packet can make a multi-hop journey with one iteration because the system
    # sorts and sends in order. So if a packet follows a chronological routing it
    # will naturally arrive at its destination.

    topThree()

main()

