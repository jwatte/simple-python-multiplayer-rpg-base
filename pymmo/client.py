
import socket
import sys
import select
import encoding



class ClientNotConnected(Exception):
    def __init__(self):
        pass


class Client(object):

    sock = -1
    inputdata = ""
    outputdata = ""
    listener = None
    addr = ""
    
    def __init__(self, name, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((name, port))
        addr = str(self.sock.getpeername())
    
    def output(self, cmd):
        if not self.isopen():
            raise ClientNotConnected()
        if not cmd.endswith("\n"):
            cmd = cmd + "\n"
        self.outputdata = self.outputdata + cmd

    def step(self):
        if not self.isopen():
            raise ClientNotConnected()
        sl = [self.sock]
        readable, writable, error = select.select(sl, sl, sl, 0)
        if readable:
            r = self.sock.recv(2048)
            self.inputdata = self.inputdata + r
            if not len(r):
                error.append(sl)
        if writable:
            n = self.sock.send(self.outputdata)
            if n < 1:
                error.append(sl)
            else:
                self.outputdata = self.outputdata[n:]
        if error:
            self.sock.close()
            self.sock = -1
        while 1:
            x = self.inputdata.partition("\n")
            if x[1]:
                self.inputdata = x[2]
                if self.listener:
                    self.listener.docmd(x[0])
                else:
                    print("no listener, received command " + x[0])
            else:
                break;
        return 1

    def isopen(self):
        return self.sock != -1
    
    def command(self, cmd):
        if not cmd.endswith("\n"):
            cmd = cmd + "\n"
        self.outputdata = self.outputdata + cmd
    
    def close(self):
        if self.isopen():
            self.sock.close()
            self.sock = -1
    
    def moveto(self, pos):
        self.command("mov " + str(pos[0]) + "," + str(pos[1]) + "," + str(pos[2]))
    
    def connect(self, name, pw):
        self.command("con " + encoding.enquote(name) + "," + encoding.enquote(pw))
    
    def idle(self):
        self.command("idl")
    
    def say(self, text):
        self.command("say " + encoding.enquote(text))


def main(argv = None):
    if (argv == None):
        argv = sys.argv
    name = "localhost"
    port = "7755"
    if len(argv) > 1:
        name = argv[1]
    if len(argv) > 2:
        port = argv[2]
    if len(argv) > 3:
        print("Warning: extra arguments ignored")
    port = int(port)
    if (port < 1) or (port > 65535):
        print("port " + str(port) + " out of range (1-65535)")
        return 1
    cli = Client(name, port)
    while 1:
        line = raw_input("> ")
        if not line:
            print("end of input")
            break
        if not cli.isopen():
            print("connection closed")
            return 1
        cli.output(line.strip())
        cli.step()
    cli.close()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

