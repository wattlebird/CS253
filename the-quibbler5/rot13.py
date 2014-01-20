alphabeta = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
rotedbeta = "nopqrstuvwxyzabcdefghijklmNOPQRSTUVWXYZABCDEFGHIJKLM"
rotdict = dict((alphabeta[i], rotedbeta[i]) for i in range(0, 52))

def rot13(s):
    newstr = ""
    for w in s[:]:
        if w in alphabeta[:]:
            newstr += rotdict[w]
        else:
            newstr += w
    return newstr
