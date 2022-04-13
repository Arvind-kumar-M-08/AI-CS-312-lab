import numpy as np
import copy
import sys
import time
from operator import itemgetter
from itertools import combinations

sys.setrecursionlimit(10000)


#INPUT FILE READING
f = open("input.txt","r")
n = f.readline()
n = n[:len(n)-1]
n = int(n)
k = f.readline()
k = k[:len(k)-1]
k = int(k)
beam_w = f.readline()
beam_w = beam_w[:len(beam_w)-1]
beam_w = int(beam_w)
if(beam_w > n):
    beam_w = n
tabu_t = f.readline()
tabu_t = tabu_t[:len(tabu_t)-1]
tabu_t = int(tabu_t)
if(tabu_t > n):
    tabu_t = n
choice = 1
f.close()

f_out = open("output.txt","w")

# 4 - SAT generator

var = [str(i) for i in range(1,n+1)]
var_bar = [str(-i) for i in range(1,n+1)]

sat = []

for i in range(k):
    clause = []
    dummy_var = var + var_bar
    for j in range(4):
        x = np.random.choice(dummy_var)
        clause.append(x)
        dummy_var.remove(x)
        y = ""
        if(x[0] == '-'):
            y = x[1:]
        if(x[0] != '-'):
            y = '-' + x
        if(y in dummy_var):
            dummy_var.remove(y)
    sat.append(clause)

f_sat = open("sat.txt","w")
for i in sat:
    for j in i:
        if(j[0] != '-'):
            f_sat.write("X")
            f_sat.write(j)
            f_sat.write(",")
        else:
            f_sat.write("~X")
            f_sat.write(j[1:])
            f_sat.write(",")
    f_sat.write("\n")

f_sat.close()

#Start state generator
start = ""
for i in range(n):
    x = np.random.choice(['0','1'])
    start += x

f_out.write("Start state\n")
f_out.write(start)
f_out.write("\n\n")

states_explored = []         #USED TO FIND NO. OF STATES EXPLORED 
uniform_sat = []             #Storing formula in a list

#Reading sat formula
f_in = open("sat.txt","r")
for i in range(k):
    string = f_in.readline()
    string = string.split(",")
    l = []
    for m in range(4):
        j = string[m]
        if(j[0]== 'X'):
            l.append(j[1:])
        else:
            j = "-" + j[2:]
            l.append(j)
    uniform_sat.append(l)

f_in.close()

#def movegen with toggling number of bits
def movegen(state, toggle):
    lst = []
    com = [i for i in range(n)]
    a = combinations(com,toggle)
    for j in a:
        new_state = copy.deepcopy(state)
        for i in j:
            if(new_state[i] == '1'):
                new_state = new_state[:i] + "0" + new_state[i+1:]
            else:
                new_state = new_state[:i] + "1" + new_state[i+1:]
        if(True):
            lst.append(new_state)
    return lst

#Heuristic function considering number of satisfying clauses
def heuristic(state):
    h = np.zeros(k,dtype=int)
    h_val = 0
    for i in range(n):
        ch = str(i)
        ch_bar = '-' + ch
        for j in range(k):
            if(state[i] == '1' and ch in uniform_sat[j] and h[j] == 0):
                h_val += 1
                h[j] = 1
            elif(state[i] == '0' and ch_bar in uniform_sat[j] and h[j] == 0):
                h_val+=1
                h[j] = 1
    return h_val

#Variable neigborhood Descent
def vnd(state):
    global states_explored
    toggle = 1

    while(toggle <= n):
        
        heap = []
        states_explored.append(state)
        
        prev_heu = heuristic(state)
        prev_state = copy.deepcopy(state)
        if(prev_heu == k):
            f_out.write("Formula is satisfiable\n")
            return state
        lst = movegen(state, toggle)
        for  i in lst:
            heap.append([i,heuristic(i)])
        state_heap = copy.deepcopy(max(heap,key=itemgetter(1)))
        state = copy.deepcopy(state_heap[0])
        if(state_heap[1] <= prev_heu):   #if current state is not better,increase toggle
            toggle = toggle + 1
            state = copy.deepcopy(prev_state)

    f_out.write("Goal state can't be reached\n")
    return state

#beam seach with width
def beam_search(state, width):
    global states_explored
    state_lst = movegen(state,1)
    heap = []
    for i in state_lst:
        heap.append([i,heuristic(i)])
    state_lst = []
    for i in range(width):
        state_heap = copy.deepcopy(max(heap,key=itemgetter(1)))
        state_lst.append(state_heap[0])
        heap.remove(state_heap)

    while(True):
        heap = []
        lst = []
        maxi = -1
        for i in state_lst:
            states_explored.append(i)
            x = heuristic(i)
            if(x>maxi):
                maxi = x
                state = i              
            if(x == k):
                f_out.write("Formula is satisfiable\n")
                return i
        for i in state_lst:
            l = movegen(i,1)
            lst.extend(l)
        if(len(lst) == 0):
            f_out.write("Local maximum\n")
            return state
        for i in lst:
            heap.append([i,heuristic(i)])
        improvement = 0
        state_lst = []
        for i in range(width):
            if(len(heap) == 0):
                break
            state_heap = copy.deepcopy(max(heap,key=itemgetter(1)))
            state_lst.append(state_heap[0])
            heap.remove(state_heap)
            if(state_heap[1]>maxi):
                improvement += 1
        if(improvement == 0):
            f_out.write("Local maximum\n")
            return state

#Movegen for Tabu with tenure t           
def movegen_tabu(state,t):
    global tenure
    best_state = ""
    best_heu = -1 
    index=-1
    for i in range(n):
        if(tenure[i] == 0):
            if(state[i] == '1'):
                new_state = state[:i] + "0" + state[i+1:]
            else:
                new_state = state[:i] + "1" + state[i+1:]
            
            h = heuristic(new_state)
            if(h>best_heu):
                index = i
                best_heu = h
                best_state = copy.deepcopy(new_state)
    if(best_state != ""):
        return [best_state,best_heu,index]
    else:
        return 0
    
#movegen to find tabu states
def movegen_restricted(state,t):
    global tenure
    best_state = ""
    best_heu = -1 
    index = -1
    for i in range(n):
        if(tenure[i] != 0):
            if(state[i] == '1'):
                new_state = state[:i] + "0" + state[i+1:]
            else:
                new_state = state[:i] + "1" + state[i+1:]
            
            h = heuristic(new_state)
            if(h>best_heu):
                index = i
                best_heu = h
                best_state = copy.deepcopy(new_state)
    if(best_state != ""):
        return [best_state,best_heu,index]
    else:
        return 0


#Tabu search
def tabu(state,t):
    global states_explored,ts,tenure 
    condition = True
    best_state = ""
    best_heuristic = -1
    while(condition == True): 
        tf = time.time()

        if(tf-ts > 10):   #Termination condition
            f_out.write("Local maximum\n")
            return state   

        states_explored.append(state)        
        prev_heu = heuristic(state)
        prev_state = copy.deepcopy(state)

        if(prev_heu > best_heuristic):  #storing the best state 
            best_state = copy.deepcopy(prev_state)
            best_heuristic = prev_heu

        if(prev_heu == k):
            f_out.write("Formula is satisfiable\n")
            return state
        next_node = movegen_tabu(state, t)

        #Aspiration condition (if all allowed states are bad then move to tabu state if it is better than best state ever.)
        res_node = movegen_restricted(state,t)
        if(res_node != 0 and res_node[1] > best_heuristic and res_node[1]>next_node[1]):
            state = copy.deepcopy(res_node[0])
            prev_heu = res_node[1]
            for i in range(n):
                if(tenure[i]!=0):
                    tenure[i] -= 1
            tenure[res_node[2]] = t
        elif(next_node != 0):
            state = copy.deepcopy(next_node[0])
            prev_heu = next_node[1]
            for i in range(n):
                if(tenure[i]!=0):
                    tenure[i] -= 1
            tenure[next_node[2]] = t
        else:
            f_out.write("Local maximum\n")
            return state
    f_out.write("Goal state can't be reached\n")
    return state


#MAIN PART

f_out.write("Variable neighbour descent\n\n")
if(choice == 1):
    state = vnd(start)
    f_out.write(state)
    f_out.write("\n")
    f_out.write("No. of states explored\n")
    f_out.write(str(len(states_explored)))
    f_out.write("\n\n")
    states_explored = []
    choice = 2

f_out.write("\nBeam search\n\n")
if(choice == 2):    
    states_explored = []
    state = beam_search(start,beam_w)
    f_out.write("width  ")
    f_out.write(str(beam_w))
    f_out.write("\n")
    f_out.write(state)
    f_out.write("\nNo. of states explored\n")
    f_out.write(str(len(states_explored)))
    f_out.write("\n\n")
    choice = 3

f_out.write("\nTabu search\n\n")
if(choice == 3):
    tenure = np.zeros(n,dtype=int)   
    ts = time.time()
    state = tabu(start,tabu_t)
    f_out.write("Tenure is ")
    f_out.write(str(tabu_t))
    f_out.write("\n")
    f_out.write(state)
    f_out.write("\nNo. of states explored\n")
    f_out.write(str(len(states_explored)))
    f_out.write("\n\n")
    states_explored = []
f_out.close()