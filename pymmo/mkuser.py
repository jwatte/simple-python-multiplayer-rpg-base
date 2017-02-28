
import cPickle as pickle
import sys
import os
import encoding
import player


try:
    sys.path.index(".")
except:
    sys.path.insert(0, ",")

import world


class BadArguments(Exception):
    msg = ""
    def __init__(self, msg):
        self.msg = msg


def main(argv = None):
    if argv == None:
        argv = sys.argv
    if len(argv) != 3:
        raise BadArguments("mkuser needs two args: username and password")
    os.chdir("data")
    user = { "password" : argv[2] }
    p = player.Player()
    p.name = encoding.safefilename(argv[1])
    user["entityrep"] = p.getrep()
    file = open("user/" + p.name, "wb")
    pickle.dump(user, file)
    print("User " + p.name + " created")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
