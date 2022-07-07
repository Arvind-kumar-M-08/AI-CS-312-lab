Travelling Salesman Problem
=============================

### Problem Statement

Given a set of cities (coordinates) and distances between them, find the best
(shortest) tour (visiting all cities exactly once and returning to the origin city) in a given amount of time,
viz. Traveling Salesman Problem.

----------------------------------

### [Report](https://github.com/Arvind-kumar-M-08/AI-CS-312-lab/blob/main/Assignment%204/11.pdf)

* Introduction and state space 

* Pseudo code for Greedy algorithm

* Ant Colony Optimization

	* Pseudo Code for ACO
	
	* Parameters used

* 2-Cities Exchange algorithm

* Approaches tried

----------------------------------

### Steps for execution 

Execute *run.sh* and give input file name

```
./run.sh
```
or
```
bash run.sh
```

#### Input 

> Sample input is attached in the same directory

#### Input Format

* *line 1 :* euclidean (or) noneuclidean

* *line 2 :* Number of cities (n)

* *Next n lines :* Coordinates of cities

* *Next n lines :* Distance to each city

----------------------------------

#### Output 

> Prints output in the terminal

#### Output Format of each tour

* *line 1 :* Tour with spaced indeces of cities

* *line 2 :* Total cost of the tour

----------------------------------

Once the time ends, prints the

> Best tour
>
> Minimum tour cost
>
> Execution time
