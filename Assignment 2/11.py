from operator import itemgetter
import copy
import sys
import time

closed =[]         #keep track of explored state
open_list = []     
heap = []          #used as min/max heap for states in OPEN list
start_state = []
goal_state = []

ts, tf = [0,0]
f = open("input.txt","r")
f_out = open("output.txt","w")

#Reading input
string = f.readline()
choice = int(string[0])
h = int(string[2])

for i in range(3):
    string = f.readline()
    list = string.split()
    start_state.append(list)

for i in range(3):
    string = f.readline()
    list = string.split()
    goal_state.append(list)

 #Dictionary to store coordinate of blocks in goal state
d_goal = dict((j,(x, y)) for x, i in enumerate(goal_state) for y, j in enumerate(i)) 

f.close()

#Heuristic 1 : considering position of blocks 
def heuristic1(curr_state):
    global goal_state, d_goal
    h_val = 0
    cur = copy.deepcopy(curr_state)
    d_cur = dict((j,(x, y)) for x, i in enumerate(cur) for y, j in enumerate(i))
    
    for i in range(3):
        for j in range(len(cur[i])):
            curx, cury = d_cur[cur[i][j]]
            goalx, goaly = d_goal[cur[i][j]]
            if( goaly == cury and goalx == curx):
                h_val += 1
            else:
                h_val -= 1
    return h_val

#Heuristic 2 : Considering heights of block
def heuristic2(curr_state):
    global goal_state, d_goal
    h_val = 0
    cur = copy.deepcopy(curr_state)
    d_cur = dict((j,(x, y)) for x, i in enumerate(cur) for y, j in enumerate(i))
    for i in range(3):
        for j in range(len(cur[i])):
            curx, cury = d_cur[cur[i][j]]
            goalx, goaly = d_goal[cur[i][j]]
            if( goaly == cury):
                h_val += (cury+1)
            else:
                h_val -=(cury+1)

    return h_val

#Heuristic 3 : Manhatten distance between start and goal state 
def heuristic3(curr_state):
    global goal_state, d_goal
    h_val = 0
    cur = copy.deepcopy(curr_state)
    d_cur = dict((j,(x, y)) for x, i in enumerate(cur) for y, j in enumerate(i))
    for i in range(3):
        for j in range(len(cur[i])):
            curx, cury = d_cur[cur[i][j]]
            goalx, goaly = d_goal[cur[i][j]]
            h_val += (abs(curx-goalx) + abs(cury-goaly)) 
    return h_val

    
#Function to find if goal state is reached or not
def goaltest(cur_state):
    global goal_state
    for i in range(3):
        if(len(goal_state[i])!=len(cur_state[i])):
            return False
        for j in range(len(goal_state[i])):
            if(goal_state[i][j]!=cur_state[i][j]):
                return False
    return True

#Returns neighbors of each state by poping and pushing all the combinations which are not in OPEN or CLOSE
def movegen(curr_state):
    global closed, open_list
    state = copy.deepcopy(curr_state)
    neighbors = []
    for i in range(len(state)):
        temp = copy.deepcopy(state)
        if len(temp[i]) > 0:
            elem = temp[i].pop()
            for j in range(len(temp)):
                temp1 = copy.deepcopy(temp)
                if j != i:
                    temp1[j] = temp1[j] + [elem]
                    if (temp1 not in closed and temp1 not in open_list):
                        neighbors.append(temp1)
    return neighbors



#BEST FIRST SEARCH FOR HEURISTIC 1,2,3
def bfs1():
    global closed, open_list, heap, start_state, goal_state
    current_state = copy.deepcopy(start_state)
    open_list.append(copy.deepcopy(start_state))
    while(True):  
        closed.append(copy.deepcopy(current_state)) 
        if(goaltest(current_state)):
            f_out.write("Goal state reached\n\n")
            return current_state
        open_list.remove(current_state) 
        prev_heu = heuristic1(current_state)
        neighbors = movegen(current_state)
        for i in neighbors:
            open_list.append(i)
            heap.append([i,heuristic1(i)])
        list = [current_state, prev_heu]
        if(list in heap):
            heap.remove(list)
        if(len(open_list) == 0):
            f_out.write("Goal state can't be reached\n\n")
            return current_state        
        current_heap = copy.deepcopy(max(heap,key=itemgetter(1)))      
        current_state = current_heap[0]


def bfs2():
    global closed, open_list, heap, start_state, goal_state
    current_state = copy.deepcopy(start_state)
    open_list.append(copy.deepcopy(start_state))
    while(True):   
        closed.append(copy.deepcopy(current_state))
        if(goaltest(current_state)):
            f_out.write("Goal state reached\n\n")
            return current_state
        open_list.remove(current_state) 
        prev_heu = heuristic2(current_state)
        neighbors = movegen(current_state)
        for i in neighbors:
            open_list.append(i)
            heap.append([i,heuristic2(i)])
        list = [current_state, prev_heu]
        if(list in heap):
            heap.remove(list)
        if(len(open_list) == 0):
            f_out.write("Goal state can't be reached\n\n")
            return current_state        
        current_heap = copy.deepcopy(max(heap,key=itemgetter(1)))      
        current_state = current_heap[0]


def bfs3():
    global closed, open_list, heap, start_state, goal_state
    current_state = copy.deepcopy(start_state)
    open_list.append(copy.deepcopy(start_state))
    while(True):   
        closed.append(copy.deepcopy(current_state))
        if(goaltest(current_state)):
            f_out.write("Goal state reached\n\n")
            return current_state
        open_list.remove(current_state) 
        prev_heu = heuristic3(current_state)
        neighbors = movegen(current_state)
        for i in neighbors:
            open_list.append(i)
            heap.append([i,heuristic3(i)])
        list = [current_state, prev_heu]
        if(list in heap):
            heap.remove(list)
        if(len(open_list) == 0):
            f_out.write("Goal state can't be reached\n\n")
            return current_state        
        current_heap = copy.deepcopy(min(heap,key=itemgetter(1)))      
        current_state = current_heap[0]


#HILL CLIMBING FOR HEURISTIC 1,2,3
def hillClimbing1():
    global closed, open_list, heap, start_state, goal_state
    current_state = copy.deepcopy(start_state)
    open_list.append(copy.deepcopy(start_state))
    while(True):   
        closed.append(copy.deepcopy(current_state))
        if(goaltest(current_state)):
            f_out.write("Goal state reached\n\n")
            return current_state
        prev_heu = heuristic1(current_state)
        neighbors = movegen(current_state)
        for i in neighbors:
            h = heuristic1(i)
            heap.append([i,h])

        current_heap = copy.deepcopy(max(heap,key=itemgetter(1)))
        if(current_heap[1] <= prev_heu):
            f_out.write("Goal state can't be reached\n\n")
            return current_state        
              
        current_state = current_heap[0]
        heap = []


def hillClimbing2():
    global closed, open_list, heap, start_state, goal_state
    current_state = copy.deepcopy(start_state)
    open_list.append(copy.deepcopy(start_state))
    while(True):   
        closed.append(copy.deepcopy(current_state))
        if(goaltest(current_state)):
            f_out.write("Goal state reached\n\n")
            return current_state
        prev_heu = heuristic2(current_state)
        neighbors = movegen(current_state)
        for i in neighbors:
            h = heuristic2(i)
            heap.append([i,h])

        current_heap = copy.deepcopy(max(heap,key=itemgetter(1)))
        if(current_heap[1] <= prev_heu):
            f_out.write("Goal state can't be reached\n\n")
            return current_state        
              
        current_state = current_heap[0]
        heap = []


def hillClimbing3():
    global closed, open_list, heap, start_state, goal_state
    current_state = copy.deepcopy(start_state)
    open_list.append(copy.deepcopy(start_state))
    while(True):   
        closed.append(copy.deepcopy(current_state))
        if(goaltest(current_state)):
            f_out.write("Goal state reached\n\n")
            return current_state
        prev_heu = heuristic3(current_state)
        neighbors = movegen(current_state)
        for i in neighbors:
            h = heuristic3(i)
            heap.append([i,h])

        current_heap = copy.deepcopy(min(heap,key=itemgetter(1)))
        if(current_heap[1] >= prev_heu):
            f_out.write("Goal state can't be reached\n\n")
            return current_state        
              
        current_state = current_heap[0]
        heap = []


#MAIN (START OF EXECUTION AFTER FILE READING)

ts = time.time()
if(choice == 0):
    if(h==0):
        cur = copy.deepcopy(bfs1())
         
    elif(h==1):
        cur = copy.deepcopy(bfs2())
         
    elif(h==2):
        cur = copy.deepcopy(bfs3())
         
    else:
        f_out.write("Enter a valid choice\n")

elif(choice == 1):
    if(h==0):
        cur = copy.deepcopy(hillClimbing1())
         

    elif(h==1):
        cur = copy.deepcopy(hillClimbing2())
         
    elif(h==2):
        cur = copy.deepcopy(hillClimbing3())
         
    else:
        f_out.write("Enter a valid choice\n")

else:
    f_out.write("Enter a valid choice\n")

tf = time.time()

#PRINTING OUTPUT FILE
f_out.write("State reached\n")
for i in cur:
    for j in i:
        f_out.write(j)
        f_out.write(" ")
    f_out.write("\n")
f_out.write("\n\nNo. of states explored\n")
states_explored = len(closed)
states_explored = str(states_explored) 
f_out.write(states_explored)
f_out.write("\n\n")
f_out.write("Time taken\n")

f_out.write(str(tf-ts))


f_out.close()        