
(TOP (S (NP (PRP it)) (VP (MD should) (VP (VB run) (ADVP (RB forever)))) (. .)))
#(TOP (S (NP (PRP it)) (VP (MD should) (VP (VB run) (ADVP (RB forever)))) (. .)))

f = open('wsj2-21.blt','r')

for line in f:
    line = line.split(' ')
    print line

