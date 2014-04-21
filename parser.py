import sys
import multiprocessing
global Rules
global Sums


def getConstituents(C,i,k):
    if i not in C:
        C[i] = dict()
    if k not in C[i]:
        C[i][k] = dict()
    return C[i][k]

def updateConstituent(C, i, k, head, rc, lc, prob):
    constituents = getConstituents(C,i,k)
    if head not in constituents:
        constituents[head] = (rc, lc, prob)
        return True
    elif constituents[head][2] < prob:
        constituents[head] = (rc, lc, prob)
        return True
    return False

def matchRulesRight(head, unary):
    global Rules
    if head not in Rules:
        return dict()

    if unary:
        return Rules[head][0]
    else:
        return Rules[head][1]

def fill(C, i, k, w):
    #pre-terminal
    if k == (i+1):
        updateConstituent(C, i, k, w[i], None, None, 1.)

    #binary rules
    for j in range(i+1,k):
        print "("+str(i)+", "+str(j)+", "+str(k)+")"
        C_right = getConstituents(C,j,k)
        for c2head in C_right:
            R_right = matchRulesRight(c2head, False)
            for lc_rhead in R_right:
                C_left = getConstituents(C,i,j)
                for c1head in C_left:
                    if c1head == lc_rhead[0]:
                        updateConstituent(C,i,k,lc_rhead[1],\
                                (c2head,C[j][k][c2head]),(c1head,C[i][j][c1head]),\
                                R_right[lc_rhead]*C_right[c2head][2]*C_left[c1head][2])
    #unary
    change = True
    while change:
        change = False
        C_main = getConstituents(C,i,k)
        for iterator in range(len(C_main.keys())):
            chead = C_main.keys()[iterator]
            R_unary = matchRulesRight(chead, True)
            for rhead in R_unary:
                change = updateConstituent(C,i,k,rhead,(chead,C[i][k][chead]),None,\
                        R_unary[rhead]*C_main[chead][2])

def parse(sentence):
    N = len(sentence)
    if N > 25:
        return "*IGNORE*"
    C = dict()
    for n in range(1, N+1):
        for i in range(N-n+1):
            print "("+str(i)+", "+str(i+n)+")"
            fill(C, i, i+n, sentence)
    return C

def addRules(count, head, rc, lc):
    global Rules
    if rc not in Rules:
        Rules[rc] = (dict(), dict())

    if lc == None:
        Rules[rc][0][head] = None
    else:
        Rules[rc][1][(lc,head)] = None

def updateSums(head, count):
    global Sums
    if head not in Sums:
        Sums[head] = count
    else:
        Sums[head] += count

def lookupSums(head):
    global Sums
    return Sums[head]

def updateRuleProb(head,rc,lc,prob):
    global Rules
    if lc == None:
        Rules[rc][0][head] = prob
    else:
        Rules[rc][1][(lc,head)] = prob

#def treefy(head, C, i, k):

def treefy(head, content, C):
    if content[1] != None:
        print head + "-->" +content[1][0]+" " +content[0][0]
        ret = treefy(content[1][0], content[1][1], C) + " "\
                + treefy(content[0][0],content[0][1],C)
    elif content[0] != None:
        print head + "-->"+content[0][0]
        ret = treefy(content[0][0], content[0][1], C)
    else:
        print "terminal-->" + head
        return head
    return "("+head+" "+ret+")"

if __name__ == '__main__':
    Rules = dict()
    Sums = dict()
    #first pass, sum counts, and add rule(head,lc,rc)
    rules_raw = open(sys.argv[1], 'r')
    for line in rules_raw:
        line = line.split()
        count = int(line[0])
        head = line[1]
        if len(line) == 5:
            lc = line[3]
            rc = line[4]
        else:
            lc = None
            rc = line[3]
        addRules(count, head, rc, lc)
        updateSums(head, count)
    rules_raw.close()

    #second pass, update probability
    rules_raw = open(sys.argv[1], 'r')
    for line in rules_raw:
        line = line.split()
        count = int(line[0])
        head = line[1]
        prob = float(count)/float(lookupSums(head))
        if len(line) == 5:
            lc = line[3]
            rc = line[4]
        else:
            lc = None
            rc = line[3]
        updateRuleProb(head,rc,lc,prob)
    rules_raw.close()

    #parsing
    sentences = open(sys.argv[2] , 'r')
    output = open(sys.argv[3], 'w')
    count = 0
    for sentence in sentences:
        sentence = sentence.split()
        C = parse(sentence)
        print treefy("TOP",C[0][len(sentence)]["TOP"],C)










