# NetworkSimulator
A system to simulate packets moving around a network. 



As part of my tutorage I have been learning about networks, my tutor
explained the underlying princibles, a rough idea of how the code
should look and left me to start building. 

At the moment the network completes one full iteration, taking account
of fibre-capacity, buffer-size and processing speed. Each packet is made
up of three parts , randomly mixed then sent round the network. If
a part is waiting at its arrival node for longer than two seconds, a 
request is made to re-send that part. 

After one full iteration all packets are accounted for, either in the buffer,
the packetsArrived list, the nodes themselves or the droppedPackets list. My
plan is to set up functionality to determine the fastest route round the network
before implementing multiple iterations. 

The system also detects packets from sent from streaming services and does not make a
request for missing parts. Instead drops the data into my droppedPackets list. 

After one iteration the system examines the time each packet
has taken to arrive at its destination. This lets us see which node 
is the best choice for any journey, from each node to the other, throughout
the network. 

This is in turn will allow the system to automatically adjust
its routing table as need arises. 
