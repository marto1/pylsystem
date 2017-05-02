from time import sleep

alphabet=["A", "B"]
axiom = "A"
rules = {"A":"ABA", 
         "B":"BB"}

def loop(axiom):
    res = ""
    for letter in axiom:
        if letter in rules:
            res += rules[letter]
    return res

while True:
    axiom = loop(axiom)
    print len(axiom)
    sleep(0.1)
