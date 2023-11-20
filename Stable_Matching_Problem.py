#Stable Matching problem: Stable Marriage/Roommates problem

#Good matching: matching that is fully stable (no unstability)
#Bad matching: matching that is quasi-stable (weakly unstable)
#Perfect matching: a matching where everybody is paired/married (bijection)

#Stable matching is not unique, order-independent and favors men (asymmetric) [tournament species]

##Hypotheses:
#Preference Asymmetry between males and females: Tournament Species hypothesis = 5% rule
#Never repeat a rejected proposal
#No cheating
#Ignoring existing pairs while proposing
#Accept a proposal if no partner
#Memory of former partners: Markov chain for Women, Tabu list for Men
#No Polygamy or Multiple partners (one-to-one bijection/monogamy)
#No Gay Uncle hypothesis
#Heterosexual only




import networkx as nx
from nxpd import draw
import numpy as np
import random
import math
import itertools
import functools



N = 20

LP = [] #Left part 
RP = [] #Right part

Vertex_Set = []
for k in range(N):
    Vertex_Set.append(k)

for j in range(N//2):
    LP.append(j)
    Vertex_Set.pop(j)
    
RP = Vertex_Set

Bipartite_Graph = {}

for k in range(N//2):
    s = int(random.uniform(0,len(RP)//2))
    f = int(random.uniform(len(RP)//2,N))
    Bipartite_Graph[k] = RP[s:f]
    
   
Marriage_Graph = np.zeros((len(LP),len(RP)))     

Married_Men = []
Unmarried_Men = LP
        
#Laissez-Faire (Deregulation method): Iterative Stabilization


def Sexual_Preference(L,R):
    LSP = [] #Men preferences
    RSP = [] #Women preferences
    for j in range(len(L)):
        random.shuffle(R)
        LV = []
        for j in range(len(R)):
            LV.append(R[j])
        LSP.append(LV)
       
    for j in range(len(R)):
        random.shuffle(L)
        RV = []
        for k in range(len(L)):
            RV.append(L[k])
        RSP.append(RV)
    return LSP, RSP

Men_Preferences = Sexual_Preference(LP,RP)[0]
Women_Preferences = Sexual_Preference(LP,RP)[1]
        
Women_Memory = [] #Markov chain
for j in range(len(RP)):
    Women_Memory.append([])
    
Men_Memory = [] #Tabu list
for j in range(len(LP)):
    Men_Memory.append([])


def Woman_Cheating(Woman,Man):
    p = 0.2 #Cheating probability: it depends on the type of species: high for pair-bonding species and low for tournament species
    th = random.uniform(0,1)
    if p > th:
        Divorce(Woman,Man)
    
    
def Man_Cheating(Man,Woman):
    l = 0.8 #Cheating probability: it depends on the type of species: low for pair-bonding species and high for tournament species
    th = random.uniform(0,1)
    if l > th:
        Divorce(Woman,Man)
    


def Accept(Woman,Man): #Accepting a partner may destroy an existing pair
    Accept = True
    Woman_Preferences = Women_Preferences[Woman]
    man_position = Woman_Preferences.index(Man)
    prob_accept = (len(Woman_Preferences) - man_position)/len(Woman_Preferences)
    th = random.uniform(0,1)
    if prob_accept >= th:
        Marriage_Graph[Man][Woman] = 1
        Marriage_Graph[Woman][Man] = 1 
        return Accept
    else:
        Accept = False
        return Accept

def Marry(Woman,Man):
    if Accept(Woman,Man) == True:
        Married_Men.append(Man)
        Unmarried_Men.pop(Unmarried_Men.index(Man))
        Men_Memory[Man].append(Woman)
        for j in range(len(Women_Memory[Woman])):
            Women_Memory.pop(j)
        Women_Memory[Woman].append(Man)
    return Accept(Woman,Man)

def Divorce(Woman,Man): #Pair destruction
    if Marriage_Graph[Man][Woman] == 1 or Marriage_Graph[Woman][Man] == 1:
        Marriage_Graph[Man][Woman] = 0
        Marriage_Graph[Woman][Man] = 0
        Married_Men.pop(Married_Men.index(Man))
        Unmarried_Men.append(Man)
    return True

def Proposal(Man): #Assuming sexually dimorphic species where males propose to females and not the other way around
    Man_Preferences = Men_Preferences[Man]
    t = 0
    w = Man_Preferences[t]
    proposal_list = [w]
    while Accept(Man,w) != True:
        t = t + 1
        w = Man_Preferences[t]
        proposal_list.append(w)
    married_woman = proposal_list[len(proposal_list)-1]
    Married = Marry(married_woman,Man)
    return [Man,married_woman]

    
         
        
def Laissez_Faire():
    #Random Matching
    tabu = []
    k = int(random.uniform(0,len(LP)))
    j = int(random.uniform(0,len(RP)))
    Marriage_Graph[k][j] = 1
    Marriage_Graph[j][k] = 1
    tabu.append([k,j])
    tabu.append([j,k])
    B = True
    while len(tabu)/2 < len(LP):
        k = int(random.uniform(0,len(LP)))
        j = int(random.uniform(0,len(RP)))
        for m in range(len(tabu)):
            B = B * bool([k,j] != tabu[m]) * bool([j,k] != tabu[m])
        while B == False:
            k = int(random.uniform(0,len(LP)))
            j = int(random.uniform(0,len(RP)))
            for m in range(len(tabu)):
                B = B * bool([k,j] != tabu[m]) * bool([j,k] != tabu[m])
        Marriage_Graph[k][j] = 1
        Marriage_Graph[j][k] = 1
        tabu.append([k,j])
        tabu.append([j,k])
        
    #Peer-to-Peer Preference-based matching: Recursive IBM
    
    #Former Partners make another pair for better mates: Iterative Stabilization [moderation law in mating systems]
    #Repeat until a stable matching is reached
    













#Gale-Shapley algorithm + Gale-Shapley theorem [Stable Matching existence theorem]
##Algorithmic Correctness: Termination, Perfect Matching and Stability

def Gale_Shapley():
    #partial matching
    #man without partner makes a proposal
    #proposal is either accepted or rejected depending on a probability threshold (acceptance may destroy an existing pair)
    #repeat until everybody is married
    ##Parameters: whom to propose? accept or reject?
    t = 0 
    M = Unmarried_Men[t]
    while len(Unmarried_Men) != 0:
        Couple = Proposal(M)
        Woman_Preferences = Women_Preferences[Couple[1]]
        Man_Preferences = Men_Preferences[M]
        WCP = True
        for j in range(len(Unmarried_Men)): #Women scan all available men (Bateman principle)
            RP = Woman_Preferences.index(Unmarried_Men[j])
            WCP = WCP * bool(RP > Woman_Preferences.index(M))
        if WCP == False:
            Woman_Cheating(Couple[1],M)
        MCP = True
        RW = Man_Preferences.index(random.choice(RP)) #Men scan only a random woman (Bataman principle)
        MCP = MCP * bool(RW > Man_Preferences.index(Couple[1]))
        if MCP == True:
            Man_Cheating(M,Couple[1])
        t = t + 1
        M = Unmarried_Men[t]
    return Marriage_Graph

        



def stableMatching(n, menPreferences, womenPreferences):
    # Do not change the function definition line.

    # Initially, all n men are unmarried
    unmarriedMen = list(range(n))
    # None of the men has a spouse yet, we denote this by the value None
    manSpouse = [None] * n                      
    # None of the women has a spouse yet, we denote this by the value None
    womanSpouse = [None] * n                      
    # Each man made 0 proposals, which means that 
    # his next proposal will be to the woman number 0 in his list
    nextManChoice = [0] * n
    
    # While there exists at least one unmarried man:
    while unmarriedMen:
        # Pick an arbitrary unmarried man
        he = unmarriedMen[0]                      
        # Store his ranking in this variable for convenience
        hisPreferences = menPreferences[he]       
        # Find a woman to propose to
        she = hisPreferences[nextManChoice[he]] 
        # Store her ranking in this variable for convenience
        herPreferences = womenPreferences[she]
        # Find the present husband of the selected woman (it might be None)
        currentHusband = womanSpouse[she]         
        
        while bool(currentHusband is None or herPreferences.index(currentHusband) > herPreferences.index(he)) == False:
        # The woman is currently unmarried, or she prefers the new proposal over her current partner
          nextManChoice[he] += 1
          she = hisPreferences[nextManChoice[he]]
          herPreferences = womenPreferences[she]
          currentHusband = womanSpouse[she] 
          
        womanSpouse[she] = he
        manSpouse[he] = she
        unmarriedMen.remove(he)
        if currentHusband is not None:
        # The woman's previous partner is now unmarried
              unmarriedMen.append(currentHusband)

           
        
        
        # Now "he" proposes to "she". 
        # Decide whether "she" accepts, and update the following fields
        # 1. manSpouse
        # 2. womanSpouse
        # 3. unmarriedMen
        # 4. nextManChoice
            
    # Note that if you don't update the unmarriedMen list, 
    # then this algorithm will run forever. 
    # Thus, if you submit this default implementation,
    # you may receive "SUBMIT ERROR".
    return manSpouse
    
# You might want to test your implementation on the following two tests:
assert(stableMatching(1, [ [0] ], [ [0] ]) == [0])
assert(stableMatching(2, [ [0,1], [1,0] ], [ [0,1], [1,0] ]) == [0, 1])

MA = stableMatching(1, [ [0] ], [ [0] ])
FA = stableMatching(2, [ [0,1], [1,0] ], [ [0,1], [1,0] ])

print(MA)
print(FA)