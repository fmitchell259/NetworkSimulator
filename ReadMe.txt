# NetworkSimulator
A system to simulate packets moving around a network. 

**26.02.2019**

As part of my tutorage I have been learning about networks, my tutor
explained the underlying princibles, a rough idea of how the code
should look and left me to start building. 

At the moment the network completes one full iteration, taking account
of fibre-capacity, buffer-size and processing speed. Each packet is made
up of three parts , randomly mixed then sent roudn the network. If
a part is waiting at its arrival node for longer than two seconds, a 
request is made to re-send that part. 

After one full iteration all packets are accounted for, either in the buffer,
the packetsArrived list, the nodes themselves or the droppedPackets list. My
plan is to set up functionality to determine the fastest route round the network
before implementing multiple iterations. 
