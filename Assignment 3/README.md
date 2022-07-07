Heuristic Search - 4-SAT Satisfiability
=============================

### Problem Statement

Generate uniform random 4-SAT for *n* variables and *k* clauses and check satisfiability using

1. Variable neighborhood descent : Modify Hill-Climbing Search to switch to a denser neighborhood function when stuck at a local optimum.

2. Beam Search : Code for different beam lengths

3. Tabu Search : Implement tabu search and find an optimum tabu tenure value for the domain.

----------------------------------

### [Report](https://github.com/Arvind-kumar-M-08/AI-CS-312-lab/blob/main/Assignment%203/11.pdf)

* Introduction, state space and goal state

* Pseudo code for movegen and goaltest function

* Heuristic function used

* Pseudocode and analysis for VND, Beam search and Tabu search

* Comparision among these by time taken

* Optimal parameters for beam search and Tabu search

----------------------------------

### Steps for execution 

#### Input 

> Modify *input.txt* given in the same directory

#### Input Format

* *line 1 :* Number of variables (int)

* *line 2 :* Number of clauses (int) 

* *line 3 :* Beam width (int)

* *line 4 :* Tabu tenure (int)

* *line 5 :* Empty

----------------------------------

#### Output 

> Writes generated 4-SAT in *sat.txt*

> Writes result in *output.txt* in the same directory




