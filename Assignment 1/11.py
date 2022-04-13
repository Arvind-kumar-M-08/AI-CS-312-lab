import sys
sys.setrecursionlimit(9000)

#global variables

choice = -1
graph= []
no_of_states = 0
length_of_path = 1
closed = []               
open_list = []            
obj_list = []
bfs_count = 0
class_count = 0
m = 0       #no of rows of maze
output = open("output1.txt","w")  #output file

#Reading input file

file_path = "input10.txt"
file = open(file_path,"r")
choice = file.readline()
choice = int(choice[0])
for i in file.readlines():
    if(len(i) != 0 and i!=" " and i!="\n"):
        m = m+1
        if(i[len(i)-1] == "\n"):
            i = i[:len(i)-1]
        graph.append(list(i))
n = len(graph[0]) #no of columns of maze

#class to store coordinate and prev, next in path

class path:
    def __init__(self, coordinate):
        self.coordinate = coordinate
        self.prev = None
        self.next = None


current_position=[0,0]   #variable to store current position
head = path([0,0])


#Function to return the neighbours
def movegen(pos):
    x,y =pos
    global closed, open_list, graph, m, n
    list = []
    if(x+1<m and (graph[x+1][y] == ' ' or graph[x+1][y]=='*') and [x+1,y] not in open_list): 
        list.append([x+1,y])
    if(x-1>0 and (graph[x-1][y] == ' ' or graph[x-1][y]=='*') and [x-1,y] not in open_list): 
        list.append([x-1,y])
    if(y+1<n and (graph[x][y+1] == ' ' or graph[x][y+1]=='*') and [x,y+1] not in open_list): 
        list.append([x,y+1])
    if(y-1>0 and (graph[x][y-1] == ' ' or graph[x][y-1]=='*') and [x,y-1] not in open_list): 
        list.append([x,y-1])
    return list

#Function to check if we have reached goal state
def goaltest(pos):
    global graph
    x,y =pos
    if(graph[x][y] == '*'):
        return True
    else:
        return False

#Function to print the output maze
def print_path(pointer):
    global graph, m, n, length_of_path, no_of_states
    graph[0][0]='0' 
    while(pointer.prev != None):
        x = pointer.coordinate
        graph[x[0]][x[1]] = '0'
        length_of_path = length_of_path +1
        pointer = pointer.prev

    no_of_states = str(no_of_states) + "\n"
    length_of_path = str(length_of_path) + "\n"
    output.write(no_of_states)
    output.write(length_of_path)
    for i in range(m):
        string=""
        for j in range(n):
            string+=graph[i][j]
        string += "\n"               
        output.write(string)
    sys.exit(0)

#Depth First Search
def dfs(pointer):
    global closed,open_list, head, current_position, no_of_states
    no_of_states = no_of_states +1
    current_position = pointer.coordinate
    closed.append(current_position)
    if(goaltest(current_position)):
        print_path(pointer)
    lst = movegen(current_position)
    for x in lst:
        open_list.append(x)
    for x in lst:
        if x not in closed:
            y = path(x)
            y.prev = pointer
            pointer.next = y
            dfs(y)

#Breadth First Search
def bfs(pointer):
    global closed, current_position, bfs_count, class_count, obj_list, no_of_states
    obj_list.append(path([0,0]))    
    while(bfs_count != len(closed)):
        no_of_states = no_of_states + 1
        current_position = obj_list[bfs_count].coordinate
        if(goaltest(current_position)):
            print_path(obj_list[bfs_count])
        lst = movegen(current_position)
        for x in lst:
            if x not in closed:
                class_count = class_count + 1
                closed.append(x)
                obj_list.append(path(x))
                obj_list[class_count].prev = obj_list[bfs_count]
                obj_list[bfs_count].next = obj_list[class_count]
        bfs_count = bfs_count + 1

#Depth First Iterative Deepening
def dfid(pointer, d):
    if(d==0):
        return
    global closed, current_position,limit, no_of_states, count, condition
    no_of_states = no_of_states +1
    count = count+1
    if(count > limit):
        condition = False
    current_position = pointer.coordinate
    closed.append(current_position)
    if(goaltest(current_position)):
        print_path(pointer)
    lst = movegen(current_position)
    for x in lst:
        open_list.append(x)
    for x in lst:
        if x not in closed:
            y = path(x)
            y.prev = pointer
            pointer.next = y
            dfid(y,d-1)


#MAIN 

if choice==0:    #BFS
    closed.append(current_position)
    bfs(head)
elif choice==1:  #DFS
    dfs(head)
elif choice==2:  #DFID
    depth = 1  
    limit = m*n
    condition = True
    while(condition):
        count = 0
        dfid(head,depth)
        depth = depth + 1
        closed = []
        open_list =[]
else:
    print("\nEnter a valid choice\n")