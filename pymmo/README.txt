
The code in this directory is copyright 2008 Jon Watte.
Released under the MIT open source license.

This code implements a very simple online RPG-style server and client in Python. 
Note that this sample is how I decided to learn Python, so it probably doesn't 
show good Python manners.

To start a (simple) server, run "python server.py"
To start a (simple) client, run "python client.py"

Client commands include:

con name,password,protoversion  : log in as a user (protoversion should be 1)
mov x,y,z                       : set desired position to x,y,z
say text                        : say something
idl                             : do nothing (keepalive for the 15 second inactive client timeout)

Two pre-created user,passwords are included: foo,1234 and bar,4321

To create a new user, run "python mkuser.py username password" which creates a
new user in the data/users directory.

If the client has a listener, the listener will be called with "docmd(self, cmd)" 
when a new command is received from the server. Commands are all of the form 
"xxx arguments" where xxx is a three-letter command code, and arguments are comma 
delimited. Commands are terminated by a single newline (\n). To be able to send 
strings that may contain commas, all command arguments are encoded with the function 
enquote() from the encoding module, and decoded using the dequote() function.

By using a binary protocol, the bandwidth of the protocol can easily be halved.


Miscellaneous bits and pieces:

server.Client is a class representing each connected user. It maintains an input 
queue and an output queue, where the input queue is tokenized into commands that end 
in newlines. The output queue is added to by various results and updates. If the 
input queue gets too long without a newline, or the output queue gets too long period, 
the client is disconnected, to protect against ill behaved clients.

world.Entity is a base class for anything in the world. When things are added to the 
world, the notifier in the server module is told about it, and an update about the 
entity is sent to each connected client. Same thing when entities are removed.

player.Player is the class that contains the Player entity for each server.Client.

client.Client is a simple class wrapping the socket connection to the server. It will 
send commands, and dispatch received commands if it has a listener.

Each Entity in the world will get a call to step() ten times a second, which is their 
chance to update their world state. Player.step() will move the position a little bit 
towards the desired position each step (currently, there's no path finding or barrier 
checking).

Server-side player data is stored per-player in a pickled dict, in a file called 
user/username in the data directory. Users are saved when they log on, and when they 
get disconnected. This means that a server crash will lose progress for users. That 
can obviously be improved -- currently, there's no good way to cleanly shut down the 
server.

The client synchronously waits for commands from the keyboard, so you should probably 
be giving the "idl" command once in a while to poll for new commands from the server 
and avoid a time-out (which is pretty short at 15 seconds).

