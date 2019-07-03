# NetworkSimulator
A system to simulate packets moving around a network. 

As part of my tutorage I have been learning about networks, my tutor
explained the underlying princibles, a rough idea of how the code
should look and left me to start building. 

My network will run for a number of "test iterations" (a global variable 
the programmer can set at the top of the script). After this the network
examines all the packets received and calucates the top three fastest
times for each journey within the network. 

These top times are accompanied by a list of nodes that were visited in 
order to achieve these times. Using this node list the network creates new
routing tables within each node (up to this point routes have been chosen
based on randomly picked "node linkage" lists).

My "active_network" switch is then turned to True and the network runs through
a number of "running iterations" (a global variable that can also be set at the
top of the script). Finally the network will print the top times for this
final iteration of the network. 

Future plans include a geentic topology generator that will use these times
to weight different shapes and sizes of networks to create an optimal solution.
