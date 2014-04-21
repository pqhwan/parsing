import sys
import multiprocessing
import time
global Rules
global Sums

global scount
global start


def getConstituents(C,i,k):
    #lazy initialization
    if i not in C:
        C[i] = dict()
    if k not in C[i]:
        C[i][k] = dict()

    return C[i][k]

def updateConstituent(Cik, head, rc, lc, prob):
    if head not in Cik:
        Cik[head] = (rc, lc, prob)
        return True
    elif Cik[head][2] < prob:
        Cik[head] = (rc, lc, prob)
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

def timeinmil():
    return int(time.time()*1000000)

def fill(C, i, k, w):
    global Rules
    global binary_time
    global unary_time
    #pre-terminal
    Cik = getConstituents(C,i,k)
    if k == (i+1):
        updateConstituent(Cik, w[i], None, None, 1.)

    #binary rules

    #print "BINARY---------"
    #print "binary starts: " + str(k-i-1) + " j values to iterate"
    binary_start =timeinmil()
    for j in range(i+1,k):
        C_right= getConstituents(C,j,k)
        #print str(len(C_right)) + " constituents in C_right"
        C_left = getConstituents(C,i,j)
        for c2head in C_right:
            if c2head not in Rules: continue
            R_right = matchRulesRight(c2head, False)
            #print "\t"+ str(len(R_right)) + " rules that have this rc value"
            for lc_rhead in R_right:
                lc = lc_rhead[0]
                if lc in C_left:
                    updateConstituent(Cik,lc_rhead[1],\
                            (c2head,C_right[c2head]),(lc,C_left[lc]),\
                            R_right[lc_rhead]*C_right[c2head][2]*C_left[lc][2])

    binary_time+= timeinmil()-binary_start
    #print"----------------"

    #print "---------unary"
    unary_start = timeinmil()
    change = True
    while change:
        change = False
        for iterator in range(len(Cik)):
            chead = Cik.keys()[iterator]
            R_unary = matchRulesRight(chead, True)
            for rhead in R_unary:
                change = updateConstituent(Cik,rhead,(chead,Cik[chead]),None,\
                        R_unary[rhead]*Cik[chead][2])
    unary_time+= timeinmil() - unary_start

def parse(sentence):
    global scount
    sentence = sentence.split()
    N = len(sentence)
    if N > 25: return "*IGNORE*"
    C = dict()
    for n in range(1, N+1):
        for i in range(N-n+1):
            #print "("+str(i)+", "+str(i+n)+")"
            fill(C, i, i+n, sentence)
    scount+=1
    print str(scount)+ " sentences done in " + str(time.time() - start) + " sec"
    return treefy("TOP",C[0][N]["TOP"], C)

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
        #print head + "-->" +content[1][0]+" " +content[0][0]
        ret = treefy(content[1][0], content[1][1], C) + " "\
                + treefy(content[0][0],content[0][1],C)
    elif content[0] != None:
        #print head + "-->"+content[0][0]
        ret = treefy(content[0][0], content[0][1], C)
    else:
        #print "terminal-->" + head
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
    scount = 0
    start = time.time()

    sentences = open(sys.argv[2], 'r')
    p = multiprocessing.Pool(processes = multiprocessing.cpu_count())
    trees = p.map(parse, sentences)
    output = open(sys.argv[3], 'w')
    for tree in trees:
        output.write(tree+'\n')

    """
    sentences = open(sys.argv[2] , 'r')
    scount = 0
    start = time.time()
    for sentence in sentences:
        #print sentence[:len(sentence)-1]
        sentence = sentence.split()
        N = len(sentence)
        if N > 25:
            print "*IGNORE*"
            continue
        else:
            binary_time = 0
            unary_time = 0
            tree = parse(sentence)
            #print "time spent on binary: " + str(float(binary_time)/1000000) + "sec"
            #print "time spent on unary: " + str(float(unary_time) /1000000) + "sec\n"
        scount+=1
        #771
    """
    sentences.close()
    output.close()










