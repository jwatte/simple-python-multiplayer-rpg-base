
import string

#   todo: this may perform poorly, but I don't have the Python-fu to do it right

dequotes = { 'n' : '\n', 'c' : ',', 's' : ';', 'w' : ' ', 't' : "\t" }
enquotes = { ',' : "\\c", ';' : "\\s", "\n" : "\\n", ' ' : "\\w", "\t" : "\\t" }


def dequote(str):
    global dequotes
    l = []
    quote = 0
    for c in str:
        if quote:
            if dequotes.has_key(c):
                l.append(dequotes[c])
            else:
                l.append(c)
            quote = 0
        else:
            if c == '\\':
                quote = 1;
            else:
                l.append(c)
    return "".join(l)


def enquote(str):
    global enquotes
    l = []
    for c in str:
        if enquotes.has_key(c):
            l.append(enquotes[c])
        else:
            l.append(c)
    return "".join(l)


# characters you don't want in file names
unsafechars = set([ ',', '.', ';', ':', '/', "\\", '?', '*' ])

def safefilename(str):
    global unsafechars
    l = []
    for c in str:
        if not (c in unsafechars):
            l.append(c)
    return "".join(l)

