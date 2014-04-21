parsing for cs146 -- hk110

[TODOS]
    #write pseudocode and declare functions
    #decide on data structure format
    #maybe unary rules must be stored separately? does this help?
    #pre-processing works fine (global Rules and Global Sums)
    #write code up to parse()
    #test it up to parse() with just one sentence
    #if the parse tree looks about right:
        #write treefy()
        #see if the final result matches the one sentence
    #got this far? nice--now try it with the whole data, get runtime

    *optimization:
        do unary

    ?multiprocessor
    ?underflow?
    ?how long does that thing take to run?


$DEFINITIONS
    #TODO the right form for search
    global Rules (head, rightchild, leftchild, probability)
        {rc : ( {(head) : probability}, {(lc,head): probabillity} )}

        #addRules(count, head, rc, lc)
        #updateRuleProb(head, rc, lc, prob)
        #matchRulesRight(head, unary?)
            True--> {(head): prob} False--> {(lc,head):prob}
        -getRuleHead(rule)
        -getRuleLeftChild(rule)
        -getRuleProb(rule)

    global Sums (head, sum)
        {rc : sum}
        #updateSums(head, count)
        #lookupSums(head)

    "C the matrix"
        C = {i:{k:{head:((rc,),(lc,),prob)}}

        -createC(N)
        #updateConstituent(C, i, k, head, rc, lc, prob)
        #getConstituents(C, i, j)
        -getConstituentHead(constituent)
        -getConstituentProb(constituent)


$MAIN
    Command line arguments
        argv[1] = data/wsj2-21.blt ("the rule")
        argv[2] = data/wsj24.txt ("termianl strings")
        argv[3] = output.txt

    preprocessing
        1. read in binarized tree-bank grammar of rules
            uhhhhh yeah
        2. construct Rule = <h (head), rightchild(rc), leftchild(lc), probability(p)>
            *make one pass through rules file, filling in <h,rc,lc> and counting sum
                global Rules
                rules_raw = open(argv[1],"r")
                for line in rules_raw:
                    line = line.split(" ")
                    count = int(line[0])
                    head = line[1]
                    if len(line) == 5:
                        lc = line[3]
                        rc = line[4]
                    else:
                        lc = None
                        rc = line[3]
                    "addRules(count,head,rc,lc)"
                    "updateSums(head, count)"
                rules_raw.close()

            *make another pass through rules file to calculate probability
                rules_raw = open(argv[1],'r')
                for line in rules_raw:
                    line = line.split()
                    count = int(line[0])
                    head = line[1]
                    prob = float(count)/float("lookupSums(head)")
                    if len(line) == 5:
                        lc = line[3]
                        rc = line[4]
                    else:
                        lc = None
                        rc = line[3]
                    "updateRuleProb(head,rc,lc,prob)"
                rules_raw.close()

    parsing
        #TODO *UNK*
        sentences = open(argv[2], "r")
        output = open(argv[3], "w")
        for sentence in sentences:
            C = "parse(sentence)"
            print treefy("TOP", C)


$PARSING_ALGORITHM:

    #takes in string literals
    def parse(w):
        w = w.split()
        N = len(w)
        C = "createC(N)"
        for n in range(1,N+1):
            for i in range(N-n):
                "fill(C, i, i+n, w)"
        return C

    def fill(C, i, k, w):
        if k == (i+1):
            "updateConstituent(C, i, k, w[i], None, None, 1.)"

        for j in range(i+1,k):
            C_right = "getConstituents(C, j, k)"
            for c_2 in C_right:
                R_right = "matchRulesRight(getConstituentHead(c_2), False)"
                for r in R_right:
                    C_left = getConstituents(C, i, j)
                    for c_1 in C_left:
                        if getConstituentHead(c_1) == "getRuleLeftChild(r)"
                            updateConstituent(C, i, k, "getRuleHead(r)", c1, c2,\
                                    "getRuleProb(r)"*"getConstituentProb(c1)"\
                                    *getConstituentProb(c2))
        change = True
        while change:
            change = False
            C_main = getConstituents(C, i, k)
            for c in C_main:
                R_unary = matchRulesright(getConstituentHead(c), True)
                for r in R_unary:
                    updateConstituent(C, i, k, getRuleHead(r), c, None,\
                            getRuleProb(r)*getConstituentProb(c))



$HELPERFUNCTIONS
----------parsing functions--------------

    treefy("TOP",C,0,len(sentence))

    def treefy(head, C, i, k):
        content = C[i][k][head]
        if content[1] != None:
            ret = treefy(content[1],C,i,k-1)+" "+treefy(content[0],C,i-1,k)
        elif content[0] == None:
            ret = treefy(content[0],C,i,k)
        else:
            return head

    def treefy(head, content, C, i, k ):
        if content[1] != None:
            #binary
            ret = treefy(content[0], C[i][k-1],C,i,k-1) + " " + treefy(content[1], ,C,i-1,k)
        elif content[0] == None:
            #unary
            ret = treefy(content[0],
        else:
            terminal-- just return





    def createC(N):
        return dict()
        *returns an NxN matrix

    def updateConstituent(C, i, k, w, rc, lc, prob):
        constituents = C[i][k]
        if head not in constituents:
            constituents[head] = (rc,lc,prob)
            return True
        elif constituents[head][2] < prob:
            constituents[head] = (rc,lc,prob)
            return True
        return False

    def getConstituents(C, i, k):
        if i not in C:
            C[i] = dict()
        if k not in C[i]:
            C[i][k] = dict()
        return C[i][k]

        #TODO make sure this works for both (C,i,j) and (C,j,k)
        *returns a list of constituents in C[a][b]
    def getConstituentHead(constituent):
        *returns the head of constituent
    def getConstituentProb(constituent):
        *returns the probability of constituent


    def matchRulesRight(head, unary):
        *returns a list of rules whose rightchild == head
        global Rules
        if unary:
            return Rules[head][0]
        else:
            return Rules[head][1]

    def getRuleHead(rule):
        *returns the head of rule
    def getRuleLeftChild(rule):
        *returns the left child of rule

    def getRuleProb(rule):
        *returns the probability of a rule

----------setup functions----------------
    def addRules(head, rc, lc)
        *adds new rule (probability is added later)
        global Rules
        if rc not in Rules:
            Rules[rc] = (dict(), dict()) #(unary, binary)

        if lc == None:
            Rules[rc][0][head] = None
        else :
            Rules[rc][1][(lc,head)] = None

        return

    def updateRuleProb(head,rc,lc,prob)
        *finds the rule head-->rc,lc and stores prob
        global Rules

        if lc == None:
            Rules[rc][0][head] = prob
        else:
            Rules[rc][1][(lc,head)] = prob

        return

    def updateSums(head, count)
        *updates sum for head
        global Sums
        Sums[head]+=count
    def lookupSums(head)
        *returns sum for head
        global Sums
        return Sums[head]

-----------cleanup functions--------------
    def filterC(C_unfiltered)
        *takes in C with all the constituents and returns the best-path version of C
        *one constituent in each C_unfiltered
    def lispify(C_filtered)
        *returns C expressed in lisp-like notation







