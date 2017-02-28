
import encoding


nextid = 1
all = {}
toadd = []
todelete = []
notify = None;
named = {}

class BadDataFormat(Exception):
    def __init__(self):
        pass


class Entity(object):
    
    id = 0
    living = 1
    pos = (0, 0, 0)
    name = None
    type = None
    
    def __init__(self, type):
        global nextid
        global toadd
        self.id = nextid
        nextid = nextid + 1;
        toadd.append(self)
        self.type = type
    
    def step(self):
        pass
    
    def die(self):
        global todelete
        if self.living:
            self.living = 0
            todelete.append(self)
    
    def onremove(self):
        pass
    
    def onadd(self):
        pass
    
    def getrep(self):
        return ",".join([self.type] + map(str, self.pos))
    
    def unpack(self, rep):
        q = rep.split(',', 4)
        if (len(q) < 4):
            raise BadDataFormat()
        self.type = encoding.dequote(q[0])
        self.pos = (float(encoding.dequote(q[1])), float(encoding.dequote(q[2])), float(encoding.dequote(q[3])))
        if (len(q) > 4):
            return q[4]
        return ""
    
    def notifylisteners(self, cmd):
        global notify
        if notify:
            notify.command(cmd)


def step():
    
    global toadd
    global all
    global todelete
    global notify
    global named
    
    for a in toadd:
        print("adding object " + str(a.id) + " " + str(a.name))
        if a.name != None:
            if named.has_key(a.name):
                prev = named[a.name]
                print("Removing previous instance of name " + a.name + " id " + str(prev.id) + " for new id " + str(a.id))
                if notify:
                    notify.removeentity(prev)
                del(all[prev.id])
                prev.onremove()
        if notify:
            notify.addentity(a)
        named[a.name] = a
        all[a.id] = a;
        a.onadd()
    toadd[:] = []
    
    for ent in all.values():
        ent.step()
    
    for d in todelete:
        print("removing object " + str(d.id) + " " + str(d.name))
        if d.name != None:
            if named.has_key(d.name):
                del(named[d.name])
        if notify:
            notify.removeentity(d)
        if all.has_key(d.id):
            del(all[d.id])
        d.onremove()
    todelete[:] = []


def dumpentities(targ):
    for ent in all.values():
        targ.dumpentity(ent)

