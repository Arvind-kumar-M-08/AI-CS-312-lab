Heuristic Search - Block World Domain
=============================

### Problem Statement

Blocks World Domain Game starts with an initial state consisting of a fixed number of blocks arranged in
3 stacks and we can move only top blocks of the stacks and we have to achieve a goal state that is a
particular arrangement of blocks by moving these blocks. Blocks World is a planning problem where we
know the goal state beforehand and the path to the Goal state is more important.

For the above domain implement the following search algorithms:
1. Best First Search :
	Try out a minimum of 3 different heuristic functions and compare the results with valid
reasoning. Use a priority queue for the OPEN list to make it computationally efficient.
2. Hill Climbing :
	With a slight modification of code, implement Hill Climbing for the domain. Compare the
performance of the two in terms of time and space.

----------------------------------

### [Report](https://github.com/Arvind-kumar-M-08/AI-CS-312-lab/blob/main/Assignment%202/11.pdf)

* Introduction, state space and goal state

* Pseudo code for movegen and goaltest function

* Heuristic functions used

* Analysis of Best First Search

* Comparision between Best First Search and Hill Climbing

----------------------------------

### Steps for execution 

#### Input 

> Modify *input.txt* given in the same directory

#### Input Format

* *line 1 :* Two spaced integers (0,1 for BFS or Hillclimbing) (0,1,2 heuristic function)

* *Next 3 lines* start state(each stack in one line) where left to right is bottom to top of stack(Each character should be spaced)

* *Next 3 lines* similarly for goal state

----------------------------------

#### Output 

> Writes result in *output.txt* in the same directory

#### Output Format

* *line 1 :* If goal state is reached or not

* *Next 3 lines :* Final reached state's stack in three lines

* *line 5 :* Number of states explored

* *line 6 :* Time taken in seconds


