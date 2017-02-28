
import world
import encoding


Player_cmds = {}

class Player(world.Entity):
    
    desiredpos = (0, 0, 0)
    
    def __init__(self, rep = None):
        world.Entity.__init__(self, "Player")
        if rep:
            self.unpack(rep)
    
    def getrep(self):
        return world.Entity.getrep(self) + "," + encoding.enquote(self.name) + \
            "," + ",".join(map(encoding.enquote, map(str, self.desiredpos)));
    
    def unpack(self, rep):
        rep = world.Entity.unpack(self, rep)
        q = rep.split(",", 4)
        if len(q) < 4:
            print("Player rep: " + rep)
            raise world.BadDataFormat()
        self.name = encoding.dequote(q[0])
        self.desiredpos = (float(encoding.dequote(q[1])), \
            float(encoding.dequote(q[2])), float(encoding.dequote(q[3])))
        if (len(q) > 4):
            return q[4]
        return ""
    
    def docmd(self, cmd):
        global Player_cmds;
        sub = cmd[:3]
        end = cmd[3:].strip()
        if Player_cmds.has_key(sub):
            (Player_cmds[sub])(self, end)
    
    def cmd_move(self, sub):
        q = sub.split(",")
        if len(q) < 3:
            print("short move command from " + self.name)
            return
        self.desiredpos = (float(encoding.dequote(q[0])), \
            float(encoding.dequote(q[1])), float(encoding.dequote(q[2])))
        self.notifylisteners("mov " + str(self.id) + "," + \
            ",".join(map(str, self.desiredpos)) + "\n")
    
    def cmd_idle(self, sub):
        #   yes, I got a command!
        pass
    
    def cmd_say(self, sub):
        self.notifylisteners("say " + str(self.id) + "," + sub + "\n")
    
    def step(self):
        # move the player towards the desired position
        world.Entity.step(self)
        p = list(self.pos)
        for i in [0, 1, 2]:
            d = self.desiredpos[i] - self.pos[i]
            if d < -0.5:
                d = 0.5
            if d > 0.5:
                d = 0.5
            p[i] = p[i] + d
        self.pos = (p[0], p[1], p[2])


Player_cmds["mov"] = Player.cmd_move
Player_cmds["idl"] = Player.cmd_idle
Player_cmds["say"] = Player.cmd_say
