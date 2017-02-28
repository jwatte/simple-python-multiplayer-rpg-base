
import socket
import select
import os
import sys
import time
import string
import encoding
import cPickle as pickle
import player


def unload(name):
    try:
        del(sys.modules[name])
        del(globals()[name])
    except:
        print(name + " wasn't a loaded module")


try:
    sys.path.index(".")
except:
    sys.path.insert(0, ".")

import world


CURRENT_PROTOCOL_VERSION = 1


acceptSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
acceptSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
acceptSocket.bind(("0.0.0.0", 7755))
acceptSocket.listen(10)

sockets = set([acceptSocket])
clients = { }


class Notifier(object):
    
    def addentity(self, ent):
        global clients
        cmd = "add " + str(ent.id) + "," + ent.getrep() + "\n";
        for cli in clients.values():
            if cli and cli.entity:
                cli.output(cmd)
    
    def removeentity(self, ent):
        global clients
        for cli in clients.values():
            if cli and cli.entity:
                cli.output("del " + str(ent.id) + "\n")
    
    def command(self, cmd):
        global clients
        for cli in clients.values():
            if cli and cli.entity:
                cli.output(cmd)

#  make sure to notify everyone
world.notify = Notifier()


start = time.clock()
now = start
last = now - 1


class Client(object):
    
    inputdata = ""
    outputdata = ""
    entity = None
    sock = -1
    state = 0
    lastcmd = 0
    addr = "unknown"
    cmds = None
    userdata = {}
    name = None
    init = 0
    
    def __init__(self, sock):
        global clients
        global sockets
        global now
        self.addr = str(sock.getpeername())
        print("New connection from " + self.addr)
        self.sock = sock
        clients[sock] = self
        sockets.update((sock,))
        self.cmds = { "con" : Client.cmd_connect }
        self.lastcmd = now
        self.init = now
    
    def step(self):
        global now
        #   attempt to parse input data
        while 1:
            t = self.inputdata.partition("\n")
            if (t[1] == ""):
                break
            self.docmd(t[0])
            self.inputdata = t[2]
        #   time out unresponsive clients
        if now - self.lastcmd > 15:
            print("Closing unresponsive client " + self.addr)
            self.close()
        elif len(self.inputdata) > 1024:
            print("Client sent too large command: " + self.addr)
            self.close()
        elif len(self.outputdata) > 8192 and self.init < now - 30:
            # the first 30 seconds are allowed to use more data
            print("Client is too laggy: " + self.addr)
            self.close()
    
    def docmd(self, cmd):
        global now
        self.lastcmd = now
        cmd3 = cmd[:3]
        if len(cmd) < 3:
            print("short command from " + self.addr + ": " + cmd)
        elif cmd3 == "bye":
            print("player requests close: " + self.name + " at " + self.addr);
            self.close()
        elif self.entity:
            self.entity.docmd(cmd)
        elif self.cmds.has_key(cmd3):
            (self.cmds[cmd3])(self, cmd[4:])
        else:
            print("unknown command from " + self.addr + ": " + cmd)
            
    def output(self, str):
        if not str.endswith("\n"):
            str = str + "\n"
        self.outputdata = self.outputdata + str
    
    def close(self):
        global sockets
        global clients
        print("Closing connection " + self.addr)
        if self.entity:
            self.savetofile()
            self.entity.die()
        sockets.difference_update((self.sock,))
        del(clients[self.sock])
        self.sock.close()
    
    def savetofile(self):
        try:
            if self.entity:
                self.userdata["entityrep"] = self.entity.getrep()
            file = open("user/" + self.name + ".tmp", "wb")
            pickle.dump(self.userdata, file)
            file.close()
            os.unlink("user/" + self.name)
            os.rename("user/" + self.name + ".tmp", "user/" + self.name)
        except Exception, x:
            print("Could not save user to file: user/" + self.name + ".tmp: " + str(x))
        
    def cmd_connect(self, arg):
        global CURRENT_PROTOCOL_VERSION
        np = arg.split(',')
        if len(np) != 3:
            print("mal-formatted connect command from " + self.addr + ": " + arg)
            return
        self.name = encoding.safefilename(encoding.dequote(np[0]))
        pw = encoding.dequote(np[1])
        proto = int(np[2])
        if (proto != CURRENT_PROTOCOL_VERSION):
            print("bad version in connect from " + self.addr + ": " + np[2])
            return
        ok = 0
        try:
            file = None
            try:
                file = open("user/" + self.name, "rb")
            except:
                pass
            if not file:
                # look for a back-up file, if we died while trying a rename() operation
                file = open("user/" + self.name + ".tmp", "rb")
            self.userdata = pickle.load(file)
            file.close()
            ok = (self.userdata["password"] == pw)
        except Exception, x:
            print("User file open exception " + str(x) + " on file " + self.name);
        if ok:
            self.entity = player.Player(self.userdata["entityrep"])
            self.userdata["lastlogin"] = time.strftime("%Y-%m-%d %H:%M:%S")
            self.output("ok! " + str(self.entity.id) + "\n")
            self.savetofile()
            world.dumpentities(self)
        else:
            self.output("fai " + encoding.enquote(self.name) + "\n")
    
    def dumpentity(self, ent):
        cmd = "add " + str(ent.id) + "," + ent.getrep() + "\n";
        self.output(cmd)



def hasdata(cli):
    return cli.outputdata

def getsock(cli):
    return cli.sock

def main():
    global now
    global last
    global sockets
    global clients
    global start
    
    os.chdir("data")

    while 1:
        #   poll 20 times a second
        try:
            csl = list(sockets)
            wr = map(getsock, filter(hasdata, clients.values()))
            readable, writable, errors = select.select(csl, wr, csl, 0.05)
        except:
            print("select() exception, sockets " + str(sockets))
            raise
        now = time.clock()
        delta = now - last
        
        #  deal with sending output queue
        for sock in writable:
            try:
                if clients.has_key(sock):
                    cli = clients[sock]
                    if cli.outputdata:
                        sent = sock.send(cli.outputdata)
                        if (sent == 0):
                            print("Nothing sent on socket " + str(sock))
                            errors.append(sock)
                        else:
                            cli.outputdata = cli.outputdata[sent:]
            except Exception, x:
                print("Socket write exception: " + str(x))
                errors.append(sock)
        
        #  deal with reading input queue
        for sock in readable:
            try:
                if clients.has_key(sock):
                    cli = clients[sock];
                    cli.inputdata = cli.inputdata + sock.recv(2048)
                else:
                    a = sock.accept()[0]
                    cli = Client(a)
            except Exception, x:
                print("Socket read exception: " + str(x))
                errors.append(sock)
        
        #  deal with errors
        for sock in errors:
            try:
                cli = clients[sock]
                if cli:
                    cli.close()
                else:
                    print ("Accept socket failed: I'm screwed!")
                    os.abort()
            except:
                pass
        
        #   step clients
        for cli in clients.values():
            if cli:
                cli.step()
        
        #   step world 10 times a second
        while delta >= 0.1:
            world.step()
            delta -= 0.1
            last += 0.1

if __name__ == "__main__":
    main()
