== Write your own MMORPG in four hours using Python!

October 4, 2008 - 09:52 — jwatte

retrieved from https://enchantedage.com/pymmo


I moderate the multiplayer and networking forum on gamedev.net. It's a pretty easy job, because most users are very polite, helpful, and well behaved. However, it seems that, monthly, someone who has never written a networked program shows up and posts their "architecture" for an "MMO" server.


"MMO" means Massively Multiplayer Online. It's a pretty hard space to develop in, not only because you need absolutely tons of content to engage thousands of users for hundreds of hours, but also because large, distributed systems are hard in general. However, that being said, most of the "architectures" will totally attempt to over-design the solution, without necessarily being grounded in experience of reality.


It has been my experience that, when you start writing a program, you don't actually know what's going to be the real challenge. You may have ideas, and maybe even experiene, but the faster you can get to something that runs, the sooner you can experiment and find out what are the actual problems. To that effect, I decided to start with "the simplest thing that could possibly work" for an "MMO" server (really, just a multi-player RPG server), and see what it looked like. However, to challenge myself a little more, I figured I'd use this as a pretext for learning the Python language, which I've only vaguely tried typing at the interpreter before.


So, at quarter past 10 in the evening, I posted one of the common replied to one of these kinds of threads. I then started downloading a Python IDE, and opened up Google with the search result for "python sockets" and started from there. At 1:30 at night, I had something working reasonably well. In three hours, while learning a new programming language, I had something where you could connect, log in, send and receive movement commands and chat. Not bad -- certainly, showing that if you start with "the simplest thing that could possibly work," you'll get to something that works pretty quickly.


Spending another hour in the morning the day after, I added a simple client interface (I had been testing the server using telnet) and packaged it up in a ZIP file. You can download the attachment to this post and take it for a spin if you want, instructions are in the "README.txt" file included. The source code is released under the MIT license, if you would ever want to re-use it, but as the code has not seen production use, I wouldn't recommend it.


So, "the simplest thing that could possibly work" is a pretty powerful design paradigm. Don't try to complicate matters until you know that they need to be complicated. In the current server, for example, users are stored one to a file, using Python dictionary pickling. There is no difference between login server, and world server, meaning it doesn't support multiple zones (or, if it does, they have to share the user database somehow).


To make this "real," you'll need a number of different improvements. Evenso, I bet you could have a 2D MMO game up and running in a week by adding the following functionality:


* Some kind of world file that loads entities into the world, and loads terrain/barriers into the world.
* Some kind of NPC entities that walk around the world.
* Character stats.
* Some way to interact with NPCs (combat and/or quests).
* A graphical front-end (client application).
* A way of registering users (probably a web page of some sort).


Now, creating all the content, and polishing the UI of the client, and load testing everything, will obviously take longer than a week. However, I think that this experiment shows pretty clearly that the challenge in getting started really is to stay focused on making something that works, rather than trying to make something that's large and complicated.
