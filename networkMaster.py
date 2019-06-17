import random, time

# Initialise the lists I need for each
# of my functions (Creating packets, sending
# packets, counting packets etc..)

resent_parts = []
node_list = []
data_type = ['Video', 'Textfile', 'Audio', 'Code', 'Image', 'Game Streaming', 'Download Data','Audio Streaming','Video Streaming']
packets_arrived = []
number_of_nodes = 6
process_time = [0, 0.2, 0.2, 0.2, 0.2, 1, 0.2]

# Fibre Link Limitations.

fibre_limits = []

for count in range(36):
    fibre_limits.append(0)

# These variables represent the amount of
# packets that can go down a particular fibre link.

one_to_two = 4000  # Index 1
one_to_four = 6000  # Index 2
two_to_three = 5500  # Index 8
two_to_one = 4000  # Index 6
two_to_six = 2700  # Index 10
three_to_two = 5000  # Index 13
three_to_five = 4500  # Index 16
four_to_one = 6000  # Index 18
four_to_five = 8000  # Index 22
four_to_six = 9000  # Index 23
five_to_three = 4500  # Index 26
five_to_four = 8000  # Index 27
five_to_six = 4700  # Index 29
six_to_two = 2700  # Index 31
six_to_four = 9000  # Index 33
six_to_five = 4700  # Index 35

# The figures are then added to each list within
# the containing fibreTrackerList.

fibre_limits[1] = one_to_two
fibre_limits[3] = one_to_four
fibre_limits[8] = two_to_three
fibre_limits[6] = two_to_one
fibre_limits[11] = two_to_six
fibre_limits[13] = three_to_two
fibre_limits[16] = three_to_five
fibre_limits[18] = four_to_one
fibre_limits[22] = four_to_five
fibre_limits[23] = four_to_six
fibre_limits[26] = five_to_three
fibre_limits[27] = five_to_four
fibre_limits[29] = five_to_six
fibre_limits[31] = six_to_two
fibre_limits[33] = six_to_four
fibre_limits[34] = six_to_five

# Initialise all my lists of lists to keep track of dropped
# and transferred packets, how many packets travel down the
# fibre link and the three best times on each route.

dropped_pack_list = []
transfer_list = []
fibre_tracker = []
time_tracker_list = []

for count in range(36):
    l = []
    transfer_list.append(l)
for count in range(36):
    fibre_tracker.append(0)

# Create another list of lists to find best times.

for count in range(36):
    best_time_list = []
    time_tracker_list.append(best_time_list)


def clear_transfer_list():

    for lists in transfer_list:
        wee_l = lists
        wee_l.clear()


def top_three_journey():

    # Start by creating two empty lists which will also hold a bunch of lists.
    # The lists within nodetracker and best_time_tracker will correspond to journeys through the network.

    node_tracker = []
    best_time_tracker = []
    top_three_packets = []

    for x in range(36):
        l = []
        for y in range(3):
            l.append(0)
        top_three_packets.append(l)

    for counting in range(36):
        node_list = []
        time_list = []
        node_tracker.append(node_list)
        best_time_tracker.append(time_list)

    # Fill up my list of lists with [0,0,0] and [999,999,999].
    # This gives me something to compare when iterating over my best_time_tracker list.

    for count13 in range(36):
        next_best_node = node_tracker[count13]
        time_list = best_time_tracker[count13]
        next_best_node.append(0)
        next_best_node.append(0)
        next_best_node.append(0)
        time_list.append(999)
        time_list.append(999)
        time_list.append(999)

    for t_list, n_list, best_list, top_list in \
            zip(time_tracker_list, node_tracker, best_time_tracker, top_three_packets):

        # Go through timeTracker and pick up a journey list.
        # Pick up the appropriate best_node and best_time list (i.e. journey 1-2, 1-3, 1-4 etc.)

        journey_list = t_list
        best_node_list = n_list
        best_time = best_list
        top_three_list = top_list

        for pack in journey_list:

            # Go through each journey_list and pick up a packet.
            # Check where it came from, where it is going and the time it took to get there.
            # This info all used to compare with our best_time and best_node list.

            packet_check = pack
            pack_arrived = packet_check.return_time_arrived()
            pack_create = packet_check.return_time_stamp()
            pack_resent = packet_check.resent

            best_node = packet_check.visited_list[0]
            time_arrived = pack_arrived - pack_create

            if pack_resent:
                break

            for ind in enumerate(best_node_list):
                if best_node in best_node_list:
                    if ind == 0:
                        if best_time[0] > time_arrived:
                            best_time[0] = time_arrived

                    elif ind == 1:
                        if best_time[1] > time_arrived:
                            best_time[1] = best_time[2]
                            best_time[2] = 999

                            best_node_list[1] = best_node_list[2]
                            best_node_list[2] = 0

                    else:
                        if best_time[2] > time_arrived:
                            best_time[2] = 999
                            best_node_list[2] = 0


            if time_arrived < best_time[2] and time_arrived < best_time[1] and time_arrived > best_time[0]:

                # Save my best time and nodes in index 2.

                time = best_time[1]
                node = best_node_list[1]

                # Shift  the best time along and set my new best time in index 2.

                best_time[2] = time
                best_time[1] = time_arrived

                # Set my new best node and set my new best node in index 2.

                best_node_list[2] = node
                best_node_list[1] = best_node

                top_three_list[1] = packet_check

            if time_arrived < best_time[2] and time_arrived < best_time[1] and time_arrived < best_time[0]:

                # Save my two best times from index 0 and index 1

                time_0 = best_time[0]
                time_1 = best_time[1]

                # Save my two best nodes from index 0 and index 1.

                node_0 = best_node_list[0]
                node_1 = best_node_list[1]

                # Shift my times along by one index and put new best time in index 0.

                best_time[1] = time_0
                best_time[2] = time_1
                best_time[0] = time_arrived

                # Shift my nodes along by one index and put new best time in index 0.

                best_node_list[1] = node_0
                best_node_list[2] = node_1
                best_node_list[0] = best_node

                top_three_list[0] = packet_check

            if time_arrived < best_time[2] and time_arrived > best_time[1]:

                # No need to save the times or nodes from other indexes,
                # just replace the last item in both lists with the best time and node.

                best_time[2] = time_arrived
                best_node_list[2] = best_node

                top_three_list[2] = packet_check

    # Using python's built in zip function I pulled the two lists together to output a tuple.
    # Each tuple represents a journey (1-2,1-3,1-4 etc) with the top three (from left to right) in each tuple.

    final_best_list = zip(node_tracker,best_time_tracker)

    # for num, journey in enumerate(final_best_list, start=1):
    #     print('Journey: ' + str(num+1) + ' : ' + str(journey))

    return final_best_list


def find_best_times(arrived_list):

    # This function DOES NOT fund the best times.
    # it simply sorts the packets into the
    # timeTracker list of lists ready for the function
    # topThree to find the BEST times.

    for p_list in arrived_list:
        packet_list = p_list
        pack = packet_list[0]
        sent_from = pack.return_sent_from()
        if sent_from == 1:
            pack_destination = pack.return_destination()
            index = pack_destination - 1
            time_tracker_list[index].append(pack)
        else:
            pack_destination = pack.return_destination()
            index = ((sent_from - 1)*6) + (pack_destination-1)
            time_tracker_list[index].append(pack)


def empty_resent():

    # I have a global resent list to keep track
    # of how may packets get resent, by each node,
    # per iteration.

    # This list needs to emptied before the next
    # iteration.

     global resent_parts

     resent_parts = []


class node:
    def __init__(self, address, process_time, node_size, buffer_size, link_table):
        self.address = address
        self.node_size = node_size
        self.process_time = process_time
        self.buffer_size = buffer_size
        self.link_table = link_table
        self.packet_list = []
        self.buffer_list = []
        self.sent_packets = []
        self.pack_received = 0
        self.pack_drop = 0
        self.pack_buff = 0
        self.forward_list = []

        self.routing_list = {1: [], 2: [],
                             3: [], 4: [],
                             5: [], 6: []}

    def return_routing_list(self):
        return self.routing_list

    def update_routing(self, top_route_list):

        index_jump = ((self.address - 1) * number_of_nodes)

        for c in range(number_of_nodes):
            new_route_list = top_route_list[c + index_jump]
            self.routing_list[c+1] = new_route_list

    def return_link_list(self, dest):

        linkage_list = self.link_table[dest]
        return linkage_list


    def return_buffer_list(self):
        return self.buffer_list

    def empty_sent_packets(self):
        self.sent_packets = []

    def empty_packet_list(self):
        self.packet_list = []

    def process_time(self):
        time.sleep(self.process_time)

    def packet_generation(self):

        # Create 1000 packets, made up of 3 sub-packets
        # for each node.

        packet_amount = 1000
        # packet_amount = random.randint(1,self.node_size)
        return_count = 0
        packet_counter = 0
        print('CREATING ' + str(packet_amount) + ' PACKETS FOR NODE ' + str(self.address))
        sent_from = self.address
        while packet_amount > 0:
            send_to = random.randint(1, 6)
            if sent_from != send_to:
                data = ''
                for count in range(3):
                    rand_num = random.randint(0, 9)
                    data = data + str(rand_num)
                packet_counter += 1
                d = random.choice(data_type)
                for count in range(3):
                    time_stamp = time.time()
                    part_num = str(str(count + 1))
                    p = packet(sent_from, send_to, data, d, time_stamp, part_num, packet_counter)
                    self.forward_list.append(p)
                    packet_amount = packet_amount - 1
                    return_count += 1

        print('we created this many packets: ' + str(packet_amount + return_count))
        random.shuffle(self.packet_list)
        return return_count

    def return_routing_path(self, dest):

        # Return a route table based on destination.

        route_table = self.link_table[dest]

        return route_table

    def sort_packets(self):

        # Import my global fibre_tracker list, this list limits
        # the amount of packets that can go down a fibre link.

        # Also import global transfer_list, this a list of lists
        # representing journey's 1-2, 1-3, 1-4 etc..

        global fibre_tracker
        global transfer_list

        # Before doing anything a node checks its buffer and brings
        # packets from there into its buffer list.

        buff_count = self.check_buff_size()
        if buff_count > 0:
            for count in range(len(self.buffer_list)):
                self.forward_list.append(self.buffer_list[count])
            self.buffer_list = []

        # Set all counters to zero to keep track of what is going where.

        transfer_count = 0
        packets_transfer_list = 0
        packets_transfer_buff = 0
        packets_transfer_drop = 0

        # My sorting algorithm works in two ways. Because my transfer_list
        # is a list of lists, I needed a wee bit of maths to pick up the
        # correct list. This works one way when the address is 1 and a
        # slightly different way when the address is greater than 1.

        # The following block sorts packets from a node's forward_list and
        # puts them in their appropriate transfer_list list. This is depending
        # on the nodes routing table, the size of the fibreLimit, and
        # the size of the buffer.

        # We also create a copy of all the packets sent to allow other nodes
        # to request a re-send if a packet has not arrived.

        if self.address == 1:
            for p in self.forward_list:
                packet = p
                dest = packet.return_destination()

                # IF active_network == False:

                possible_nodes = self.return_routing_path(dest)
                selected_node = random.choice(possible_nodes)

                index = selected_node - 1

                if fibre_tracker[index] < fibre_limits[index]:
                    fibre_tracker[index] += 1
                    transfer_list[index].append(packet)
                    self.sent_packets.append(packet)
                    packets_transfer_list += 1
                else:
                    buff_count = self.check_buff_size()
                    if buff_count < self.buffer_size:
                        self.buffer_list.append(p)
                        packets_transfer_buff += 1
                    else:
                        dropped_pack_list.append(p)
                        packets_transfer_drop += 1

                # TODO:      SELECT FROM ROUTING LIST.
                # TODO:      USE WEE MATHS TO PICK RIGHT LIST.
                # TODO:      COMPLETE COMPARISONS ON EACH SENDING NODE.
                # TODO:      IF CAN GO TO INDEX 0, SEND, OTHERWISE 1
                # TODO:      OTHERWISE 2, OTHERWISE DROP.

        else:
            for p in self.forward_list:
                packet = p
                dest = packet.return_destination()
                possible_nodes = self.return_routing_path(dest)
                random_node = random.choice(possible_nodes)
                index = ((self.address - 1) * number_of_nodes) + (random_node - 1)
                if fibre_tracker[index] < fibre_limits[index]:
                    fibre_tracker[index] += 1
                    transfer_list[index].append(packet)
                    self.sent_packets.append(packet)
                    packets_transfer_list += 1
                else:
                    buff_count = self.check_buff_size()
                    if buff_count < self.buffer_size:
                        self.buffer_list.append(p)
                        packets_transfer_buff += 1
                    else:
                        dropped_pack_list.append(p)
                        packets_transfer_drop += 1

        # Empty the forward_list, ready for the next iteration of packets.

        self.forward_list = []

        # Return total packets transferred out of node.

        return transfer_count

    def check_packet_parts(self):

        # Create a checking_list, this will be populated by
        # packets that have been waiting longer than 2 seconds.

        checking_list = []
        now = time.time()
        resend_parts = 0
        streamed_parts_removed = 0

        # Check if a packet in a nodes packetList has been waiting longer
        # then two seconds, if so, add it to checking_list.

        for p in self.packet_list:
            packet = p
            if abs(now - packet.return_time_arrived()) > 1.0:
                checking_list.append(packet)

        # Set my control variable check_length, this will be used
        # to check each packet in the checking_list has every part.

        check_length = len(checking_list)

        # Iterate over checking_list until all packets have been checked
        # for all parts.

        # We put each packet in a part_list and then check for all three
        # parts. If we find all three the part_list containing all three
        # of our packet parts is added to global packets_arrived list.

        while check_length > 0:
                part_list = []
                packet = checking_list[0]
                part_num = packet.return_part_num()
                sent_from = packet.return_sent_from()
                packet_num = packet.return_packet_num()
                part_list.append(packet)

                for countThree in range(1, check_length):
                    packet2 = checking_list[countThree]
                    packet2_num = packet2.return_packet_num()
                    packet2_part = packet2.return_part_num()
                    pack2_from = packet2.return_sent_from()
                    if packet2_num == packet_num and pack2_from == sent_from and packet2_part != part_num:
                        part_list.append(packet2)

                if len(part_list) == 3:
                    for mini_pack in part_list:
                        if mini_pack in self.packet_list:
                            self.packet_list.remove(mini_pack)
                        if mini_pack in checking_list:
                            checking_list.remove(mini_pack)

                        mini_pack.record_time_arrived()

                    packets_arrived.append(part_list)

                    # Always adjust check_length when removing packets.

                    check_length = check_length - 3

                else:
                    # If we don't have all three parts then we need to
                    # first check if the packet is sa 'Streaming' packet.

                    # If the packet is not a streaming packet we must
                    # request a re-send.

                    # Pick up one of the parts of the packet in part_list.
                    # Check if this packet has 'Stream' in it's data-type.

                    stream_check_pack = part_list[0]
                    stream_check_data = stream_check_pack.return_data_type()

                    # If we find the word 'Stream' then remove that part.
                    # Also remove this packet from the packetList.
                    # Streaming packets are lossy data and as such can be dropped

                    if 'Stream' in stream_check_data:
                        for pack in part_list:
                            if pack in checking_list:
                                checking_list.remove(pack)
                                streamed_parts_removed += 1
                                check_length = check_length - 1
                            if pack in self.packet_list:
                                self.packet_list.remove(pack)
                    else:
                        part_check_list = [1, 2, 3]
                        part_got_list = []
                        sent_from_node = part_list[0].return_sent_from()
                        packet_num = part_list[0].return_packet_num()

                        # The part_list contains packet objects so a loop is required
                        # to produce a part_got_list of each packet's part number.

                        for wee_packs in part_list:
                            part_num = int(wee_packs.return_part_num())
                            part_got_list.append(part_num)

                        # Using 'symmetric_difference' and 'set' we can then produce a
                        # final list of the parts we need to request from various nodes.

                        # This is merging my checkPartParts and my part_got_list, to give
                        # me merged_list, showing the differences between the two. i.e
                        # the parts I need to re-request.

                        merged_list = list(set(part_got_list).symmetric_difference(set(part_check_list)))

                        # The following just allows me to count how many packets
                        # are being re-sent.

                        how_many = 3 - len(merged_list)

                        if how_many == 1:
                            resend_parts += 1
                        elif how_many == 2:
                            resend_parts += 2

                        # Go over my checking list and remove the packets
                        # I have in the part_list.

                        for pack in part_list:
                            checking_list.remove(pack)

                        # Always adjust my control variable (check_length) when removing
                        # packets from the checking_list.

                        check_length = len(checking_list)

                        # Finally request a re-send of one or two parts of a packet.

                        for tup in merged_list:
                            node_list[sent_from_node].resend_part(packet,packet_num, tup)

        # Reset time-stamps on packets awaiting a re-send.

        for packs in self.packet_list:
            packet = packs
            packet.reset_time_stamp()
            packet.record_time_arrived()

        print('THIS IS NODE: ' + str(self.address) + " REMOVED THIS MANY STREAM PACKETS: " + str(streamed_parts_removed))

    def resend_part(self,packet, pack_num, part_num):

        # Iterate over a nodes sentPackets list and
        # find the missing packet. Consult that nodes
        # routing table and re-send.

        for p in self.sent_packets:
            packet = p
            packet_num = int(packet.return_packet_num())
            if packet_num == pack_num:
                part_number = int(packet.return_part_num())

                if part_number == part_num:
                    dest = packet.return_destination()
                    possible_nodes = self.return_routing_path(dest)
                    random_node = 0
                    while random_node == 0:
                        random_node = random.choice(possible_nodes)
                        if random_node != 0:
                            packet.resent = True
                            node_list[random_node].receive_packet(packet)
                            resent_parts.append(packet)

        # Once a re-send has been completed, delete that packet
        # from the sentPackets list.

        if packet in self.sent_packets:
            self.sent_packets.remove(packet)

    def receive_packet(self, packet):

        if packet in self.forward_list:
            dropped_pack_list.append(packet)
            self.forward_list.remove(packet)

        if packet in self.packet_list:
            dropped_pack_list.append(packet)
            self.packet_list.remove(packet)

        # As soon as a packet is received we add that
        # node to the packets visited_list. This lets us
        # keep track of which nodes a packet has visited.


        packet.add_visit(self.address)

        # Work out where this packet is destined for?

        dest = packet.return_destination()

        # If the packet has not arrived, record its time
        # of arrival and add to that nodes packetList.

        # If the packet still needs to continue on its
        # journey put the packet in that nodes forward_list.

        if self.address == dest:
            packet.record_time_arrived()
            self.packet_list.append(packet)
            self.pack_received += 1
        else:
            self.forward_list.append(packet)


    def check_buff_size(self):
        return len(self.buffer_list)

    def send_packets(self):

        # Import my transfer_list. This is my list of lists
        # representing the journey's through the network.
        # After a node has sorted its packets these lists are all
        # full of packets ready to be sent to their respective nodes.

        global transfer_list

        # This second_range is the small piece of maths I have
        # used to pick up the right list of lists index. This
        # only needs to be used when the address is greater than 1.

        second_range = (self.address - 1) * number_of_nodes

        packets_moved = 0

        # Iterate over transfer_list, pick up a journey list
        # and send the packets on their way.

        if self.address == 1:
            for count in range(number_of_nodes):
                dest_list = transfer_list[count]
                dest_node = count + 1
                for countTwo in range(len(dest_list)):
                    node_list[dest_node].receive_packet(dest_list[countTwo])
                    packets_moved += 1
        else:
            for count in range(number_of_nodes):
                dest_list = transfer_list[second_range+count]
                dest_node = count + 1
                for countTwo in range(len(dest_list)):
                    node_list[dest_node].receive_packet(dest_list[countTwo])
                    packets_moved += 1


class packet:
    def __init__(self, sent_from, send_to, data, data_type, time_stamp, part_num, packet_num):
        self.sent_from = sent_from
        self.send_to = send_to
        self.data = data
        self.data_type = data_type
        self.time_stamp = time_stamp
        self.packet_num = packet_num
        self.part_num = part_num
        self.time_arrived = 0.0
        self.visited_list = []
        self.resent = False

    # Below are a series of small functions
    # that return various information about a packet.

    def return_routing_path(self):
        return self.visited_list

    def return_time_arrived(self):
        return self.time_arrived

    def return_packet_num(self):
        return self.packet_num

    def return_part_num(self):
        return self.part_num

    def add_visit(self, node_number):
        self.visited_list.append(node_number)

    def reset_time_stamp(self):
        time_stamp = time.time()
        self.time_stamp = time_stamp

    def record_time_arrived(self):
        now = time.time()
        self.time_arrived = now

    def return_sent_from(self):
        return self.sent_from

    def return_data_type(self):
        return self.data_type

    def return_destination(self):
        return self.send_to

    def return_time_stamp(self):
        return self.time_stamp


def main():

    # Import global node_list.
    # This allows me to access all the methods associated with any particular node from anywhere within the system.

    global node_list

    # Create my six nodes.
    # Node zero is created and never used to allow for consistent numbers.

    nodeZero = node(0, 0, 0, 0, 0)
    node_list.append(nodeZero)
    node_one = node(1, 0.2, 1010, 1200, {1: [], 2: [2], 3: [2,4], 4: [4], 5: [2, 4], 6: [2, 4]})
    node_list.append(node_one)
    node_two = node(2, 0.2, 1010, 800, {1: [1], 2: [], 3: [3], 4: [1, 3, 6], 5: [1, 3, 6], 6: [6]})
    node_list.append(node_two)
    node_three = node(3, 0.2, 1010, 1100, {1: [2, 5], 2: [2], 3: [], 4: [2, 5], 5: [5], 6: [2, 5]})
    node_list.append(node_three)
    node_four = node(4, 0.2, 1010, 1500, {1: [1], 2: [1, 5, 6], 3: [1, 5, 6], 4: [], 5: [5], 6: [6]})
    node_list.append(node_four)
    node_five = node(5, 1, 1010, 650, {1: [3, 4, 6], 2: [3, 4, 6], 3: [3], 4: [4], 5: [], 6: [6]})
    node_list.append(node_five)
    node_six = node(6, 0.2, 1010, 1270, {1: [2, 4, 5], 2: [2], 3: [2, 4, 5], 4: [4], 5: [5], 6: []})
    node_list.append(node_six)

    # Create packets within each node.
    # A node cannot create a packet destined for itself.
    # Print statements to allow developer to track packets.

    node_one_gen = node_one.packet_generation()
    print(str(node_one_gen) + ' packets generated in Node 1.')
    node_two_gen = node_two.packet_generation()
    print(str(node_two_gen) + ' packets generated in Node 2.')
    node_three_gen = node_three.packet_generation()
    print(str(node_three_gen) + ' packets generated in Node 3.')
    node_four_gen = node_four.packet_generation()
    print(str(node_four_gen) + ' packets generated in Node 4.')
    node_five_gen = node_five.packet_generation()
    print(str(node_five_gen) + ' packets generated in Node 5.')
    node_six_gen = node_six.packet_generation()
    print(str(node_six_gen) + ' packets generated in Node 6.')

    total_pack = node_one_gen + node_two_gen + node_three_gen + node_four_gen + node_five_gen + node_six_gen
    print(' TOtal packages created : ' + str(total_pack))

    # Start the process of sending packets.Each node sorts the packets
    # in their packetList.
    #
    # The packets get transferred to a global transfer_list, sorted into
    # journey (1-2, 3-5, 4-2 etc...).
    #
    # Packets are then taken from each respective journey list and sent
    # to their respective nodes. The sleep function aims to imitate the
    # time for a node to process the data.

    for count in range(10):
        node_one.sort_packets()
        node_one.send_packets()
        time.sleep(process_time[1])

        node_two.sort_packets()
        node_two.send_packets()
        time.sleep(process_time[2])

        node_three.sort_packets()
        node_three.send_packets()
        time.sleep(process_time[3])

        node_four.sort_packets()
        node_four.send_packets()
        time.sleep(process_time[4])

        node_five.sort_packets()
        node_five.send_packets()
        time.sleep(process_time[5])

        node_six.sort_packets()
        node_six.send_packets()
        time.sleep(process_time[6])

        # When all packets have been sorted   / vb,vbb,.and sent they are held in a nodes checking_list.
        # This allows for a node to check that all 'parts' of a packet have been received.
        # If a packet has been waiting longer than 2 seconds it will be checked for completeness.
        # If a packet is complete it will be removed from the node completely and added to the global packets_arrived list.
        # Items in this list comprise a list of three 'parts' of a packet (which are packet objects themselves).

        node_one.check_packet_parts()
        node_two.check_packet_parts()
        node_three.check_packet_parts()
        node_four.check_packet_parts()
        node_five.check_packet_parts()
        node_six.check_packet_parts()

        # After each iteration I need to empty the list that collects each resent part.
        # This global list is used to count the number of packets a node resends.

        # After one iteration I need to reset this list to keep count of the total packets
        # resent with multiple iterations.

        # Transfer list needs cleared before the next iteration can start.

        clear_transfer_list()

        print('Total Number of resent Packets: ' + str(len(resent_parts)) + '\n')
        empty_resent()

        # The following print statements and method calls allow the developer to ensure
        # their are no missing packets, or duplicate packets, within the system.

        # The total packets in a nodes packetList, bufferlist and any packets dropped should
        # be equal to the total packets created plus the number of packets re-requested.

        node_one.empty_sent_packets()
        node_two.empty_sent_packets()
        node_three.empty_sent_packets()
        node_four.empty_sent_packets()
        node_five.empty_sent_packets()

    print('-------------------------------------------\n')

    total_arrived = len(packets_arrived)

    print('TOTAL PACKETS ARRIVED AT DESTINATION: ' + str(total_arrived) + '\n')
    print('TOTAL PACKETS CREATED: ' + str(total_pack))
    print('TOTAL PACKETS ARRIVED: ' + str(total_arrived))
    print('-------------\n')
    print('---------------------------')
    print('PACKAGES LEFT IN NODE ONE FORWARD LIST: ' + str(len(node_one.forward_list)))
    print('--------------------------')
    print('PACKAGES LEFT IN NODE TWO FORWARD LIST: ' + str(len(node_two.forward_list)))
    print('--------------------------')
    print('PACKAGES LEFT IN NODE THREE FORWARD LIST: ' + str(len(node_three.forward_list)))
    print('--------------------------')
    print('PACKAGES LEFT IN NODE FOUR FORWARD LIST: ' + str(len(node_four.forward_list)))
    print('--------------------------')
    print('PACKAGES LEFT IN NODE FIVE FORWARD LIST: ' + str(len(node_five.forward_list)))
    print('--------------------------')
    print('PACKAGES LEFT IN NODE SIX FORWARD LIST: ' + str(len(node_six.forward_list)))

    node_oneBuff = node_one.return_buffer_list()
    node_twoBuff = node_two.return_buffer_list()
    node_threeBuff = node_three.return_buffer_list()
    node_fourBuff = node_four.return_buffer_list()
    node_fiveBuff = node_five.return_buffer_list()
    node_sixBuff = node_six.return_buffer_list()

    print('------------------------------')
    print('TOTAL LEFT IN BUFFER ONE: ' + str(len(node_oneBuff)))
    print('TOTAL LEFT IN BUFFER TWO: ' + str(len(node_twoBuff)))
    print('TOTAL LEFT IN BUFFER THREE: ' + str(len(node_threeBuff)))
    print('TOTAL LEFT IN BUFFER FOUR: ' + str(len(node_fourBuff)))
    print('TOTAL LEFT IN BUFFER FIVE: ' + str(len(node_fiveBuff)))
    print('TOTAL LEFT IN BUFFER SIX: ' + str(len(node_sixBuff)))
    print('')
    print('--------------------------------')
    print('SIZE OF DROPPED PACKET LIST: ' + str(len(dropped_pack_list)))
    print('--------------------------------')

    print('FIBRE LIMIT LIST: ' + '\t' + str(fibre_limits[::]))
    print('FIBRE TRACKER LIST: ' + str(fibre_tracker[::]))

    print('---------------------------')
    print('PACKAGES LEFT IN NODE ONE PACKET LIST: ' + str(len(node_one.packet_list)))
    print('--------------------------')
    print('PACKAGES LEFT IN NODE TWO PACKET LIST: ' + str(len(node_two.packet_list)))
    print('--------------------------')
    print('PACKAGES LEFT IN NODE THREE PACKET LIST: ' + str(len(node_three.packet_list)))
    print('--------------------------')
    print('PACKAGES LEFT IN NODE FOUR PACKET LIST: ' + str(len(node_four.packet_list)))
    print('--------------------------')
    print('PACKAGES LEFT IN NODE FIVE PACKET LIST: ' + str(len(node_five.packet_list)))
    print('--------------------------')
    print('PACKAGES LEFT IN NODE SIX PACKET LIST: ' + str(len(node_six.packet_list)))
    print('--------------------------\n')

    # The function find_best_times gets packets out of the packets_arrived list and
    # puts them into my timeTracker list of lists (a list of journeys).

    find_best_times(packets_arrived)

    # The function topThree iterates over each sorted timeTracker packet and creates
    # a top three fastest packets for each journey in the network.

    # A packet can make a multi-hop journey with one iteration because the system
    # sorts and sends in order. So if a packet follows a chronological routing it
    # will naturally arrive at its destination.

    best_list = top_three_journey()
    saved_best = []

    # Zipped objects can only be unpacked once, so I have saved a copy into saved_best.

    for num, journey in enumerate(best_list, start=1):
        saved_best.append(journey)
        print('Journey: ' + str(num+1) + ' : ' + str(journey))

    # Initialise a separate list to hold only the next_best_node list for each journey.

    node_j_list = []

    # Pull each best_node_list from each tuple within my saved list.

    for tup in saved_best:
        tup_choice = tup
        node_j = tup_choice[0]
        node_j_list.append(node_j)

    # Some test print statements to check my update_routing function.
    # ---------------------------------------------------------------
    # TODO: MUST REMOVE DUPLICATES FROM EACH LIST IN SEPARATE FUNCTION.
    #       I WILL DO THIS BY CREATING AN UPDATE WITHIN THE NODE. THIS
    #       WAY EACH NODE CAN CALL ITS LINK DICTIONARY AS REFERENCE.

    print("Node routing_list before receiving top times.\n")

    for n, nod in enumerate(node_list, start=1):
        print("Node: " + str(n) + " Routing Table.\n")
        dict = nod.return_routing_list()
        print(dict)

    print("Updating....\n")

    for n in node_list:
        n.update_routing(node_j_list)

    print("Node One routing_list after receiving top times.\n")

    for n, nod in enumerate(node_list, start=1):
        print("Node: " + str(n) + " Routing Table.\n")
        dict = nod.return_routing_list()
        print(dict)


main()





