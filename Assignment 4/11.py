import sys, copy
import numpy as np
from operator import itemgetter
import time

#READING INPUT FILE

ti = time.time()
tf = 0
filename = sys.argv[1]
f_in = open(filename,"r")
choice = f_in.readline()
choice = choice[:len(choice)-1]
vertices = f_in.readline()
vertices = int(vertices[:len(vertices)-1])
coordinates = []
tours =[]
for _ in range(vertices):
    line = f_in.readline()
    line = line[:len(line)-1]
    line = line.split()
    line[0] = float(line[0])
    line[1] = float(line[1])
    coordinates.append(line)

v_dist = []
for _ in range(vertices):
    line = f_in.readline()
    line = line[:len(line)-1]
    line = line.split()
    for i in range(vertices):
        line[i] = float(line[i])
    v_dist.append(line)

no_of_greed = vertices

def printing_tour(tour):
    for i in range(vertices):
        print(tour[i],end=" ")
    print(end='\n')

#GREEDY CONSTRUCTIVE METHOD

def greedy():
    global coordinates, v_dist, tours,no_of_greed
    min_total = float('inf')
    if(vertices < 251):
        no_of_greed = vertices
    else:
        no_of_greed = 100
    for i in range(no_of_greed):
        closed = []
        closed.append(i)
        visited = 1
        total_distance = 0
        while(visited<vertices):
            current = closed[visited-1]
            # MOVEGEN 
            min_dist = float('inf')
            min_city = -1
            for j in range(vertices):
                if(j not in closed and v_dist[current][j] < min_dist):
                    min_dist = v_dist[current][j]
                    min_city = j
        
            visited = visited+1
            closed.append(min_city)
            total_distance += v_dist[current][min_city]
            current = min_city
        
        total_distance += v_dist[current][i]
        if(total_distance < min_total):
            min_total = total_distance 

        dummy = [closed,total_distance]
        tours.append(dummy)       



if(choice == "euclidean" or choice == "noneuclidean"):
    greedy()
else:
    print("Invalid input")

# ANT COLONY OPTIMIZATION

mult_cons = vertices/100
no_of_ants = 100
q = 35*mult_cons
q_big = 100*mult_cons
alpha = 1
beta = 5
pheromone = np.zeros([vertices,vertices],dtype=float)
delta = 0.3
min_tour = min(tours,key=itemgetter(1))
min_tour_cost = min_tour[1]

if(time.time()-ti > 280):
    print("\n\nBEST TOUR\n\n")
printing_tour(min_tour[0])
print("tour cost : ",min_tour[1])
if(time.time()-ti > 280):
    print("time of execution : ",time.time()-ti)
    sys.exit(0)

for i in range(no_of_greed):
    ant_tour = copy.deepcopy(min(tours,key=itemgetter(1)))
    tours.remove(ant_tour)
    for j in range(vertices-1):
        pheromone[ant_tour[0][j]][ant_tour[0][j+1]] += float(1800*mult_cons/ant_tour[1])

pheromone += 0.01
min_path = min_tour[0][:]
def aco():
    global probability, pheromone, alpha, beta, q, no_of_ants, vertices,v_dist,delta, min_tour_cost,q_big,min_path

    while(time.time()- ti < 25*mult_cons):

        tour_list = []       
        for n in range(no_of_ants):
            tour = []
            tour_cost = 0
            cities = [i for i in range(vertices)]
            start = np.random.choice(cities)
            cities.remove(start)
            tour.append(start)
            current = start
            
            for j in range(vertices-1):
                probability = []
                prob_sum = 0
                for k in cities:
                    x = float((pheromone[current][k]**alpha)*((1/v_dist[current][k])**beta))
                    probability.append(x)
                    prob_sum += x
                
                for k in range(len(cities)):
                    probability[k] = probability[k]/prob_sum
                next_city = np.random.choice(cities,p = probability)
                tour_cost += v_dist[current][next_city]
                tour.append(next_city)
                current = next_city
                cities.remove(current)
            
            tour_cost += v_dist[current][start]
            if(tour_cost < min_tour_cost):
                min_path = tour[:]
                min_tour_cost = tour_cost
                if(time.time()-ti > 280):
                    print("\n\nBEST TOUR\n\n")
                printing_tour(tour)
                print("tour cost : ",min_tour_cost)
                if(time.time()-ti > 280):
                    print("time of execution",time.time()-ti)
                    sys.exit(0)
            tour_list.append([tour,tour_cost])

            #Updating pheromone
        new_pheromone = np.zeros([vertices,vertices],dtype=float)
        for m in range(no_of_ants):
            for j in range(vertices-1):
                if(tour_list[m][1] == min_tour_cost):
                    new_pheromone[tour_list[m][0][j]][tour_list[m][0][j+1]] += q_big/tour_list[m][1]
                else:
                    new_pheromone[tour_list[m][0][j]][tour_list[m][0][j+1]] += q/tour_list[m][1]
            if(tour_list[m][1] == min_tour_cost):
                new_pheromone[tour_list[m][0][vertices-1]][tour_list[m][0][0]] += q_big/tour_list[m][1]
            else:
                new_pheromone[tour_list[m][0][vertices-1]][tour_list[m][0][0]] += q/tour_list[m][1]
        
        for i in range(vertices):
            for j in range(vertices):
                pheromone[i][j] = float(delta*pheromone[i][j]) + new_pheromone[i][j]
    
if(vertices <= 100):
    aco()

# 2 CITIES EXCHANGE

def city_exchange(path, i, j):
    temp = path[i:j]
    for k in range(i, j):       
        path[k] = temp[j-k-1]
    return path

if(time.time()-ti > 280):
    print("\n\nBEST TOUR\n\n")
    printing_tour(min_path)
    print("tour cost : ",min_tour_cost)
    print("time of execution : ",time.time()-ti)
    sys.exit(0)

for i in range(vertices):
    for j in range(i):
        path = min_path[:]       
        path = city_exchange(path, j, i)
        cost = 0
        for x in range(vertices-1):
            cost += v_dist[path[x]][path[x+1]]
        cost += v_dist[path[vertices-1]][path[0]]
        if min_tour_cost>cost:
            min_tour_cost = cost
            min_path = path[:]
            if(time.time()-ti > 280):
                print("\n\nBEST TOUR\n\n")
            printing_tour(min_path)
            print("tour cost : ",cost)
            if(time.time()-ti >280):
                print("time of execution : ",time.time()-ti)
                sys.exit(0)

# 3 CITIES EXCHANGE

def city_exchange3(path, i, j, k):
    temp = []
    for x in range(0, i):
        temp.append(path[x])
    for x in range(j, k):
        temp.append(path[x])
    for x in range(i, j):
        temp.append(path[x])
    for x in range(k, len(path)):
        temp.append(path[x])
    return temp

for i in range(vertices):
    for j in range(i):
        for k in range(j):
            path = min_path[:]        
            path = city_exchange3(path, k, j, i)
            cost = 0
            for x in range(vertices-1):
                cost += v_dist[path[x]][path[x+1]]
            cost += v_dist[path[vertices-1]][path[0]]
            if min_tour_cost>cost:
                min_tour_cost = cost
                min_path = path[:]
                if(time.time()-ti > 280):
                    print("\n\nBEST TOUR\n\n")
                printing_tour(min_path)
                print("tour cost : ",cost)
                if(time.time()-ti > 280):
                    print("time of execution : ",time.time()-ti)
                    sys.exit(0)
print("\n\nBEST TOUR\n\n")
printing_tour(min_path)
print("tour cost : ",min_tour_cost)
print("time of execution : ",time.time()-ti)