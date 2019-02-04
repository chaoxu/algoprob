# Algorithmic Problems and Exercises

## Motivation

This is an ongoing document consists of problems and exercises in algorithms that fits my own preference.
The goal is to create an exercise book. 
It should also be a quick reference for the fastest algorithm known for the problem.

It is motivated by my frustration that I often see a problem, but forgot what is known about the best running time. 
Exercises help me to derive the most important steps to get the optimal algorithm.

## Scope

The document has extreme biased toward my own taste.
To keep myself sane, there is some scope involved.  

For problems, we mostly focus on decision problems and optimization problem.
Also for optimization problems, we want to find the value instead of the structure the gives the value.
If the search problem or the function problem is strictly harder, then we will note it.
Purely numerical problems are not studied. 
Enumeration and counting problems are rarely covered. 

We are only interested in classic sequential algorithms. We do not care about space complexity, cache performance, real-time property, basically anything not related to the sequential time complexity.

We are only interested in polynomial time algorithms, or sometimes pseudopolynomial time algorithms.
For optimization problems, strongly polynomial time algorithms are preferred. 

We are only interested in deterministic algorithms. So there will be no randomization. However for analysis proposes, probability might be used.
The problems should be fundamental, used as subroutine for many different problems, or can be used to demonstrate a general technique. 

The model of computation is usually the Word RAM. But the weaker the model the more interesting.
Often, we consider the algebraic complexity, which is the number of the arithmetic operations.
For computational geometry problems, we consider the Real RAM.

For data structures, optimal amortized running time is sufficient.
We rarely care about dynamic problems, unless it can be used to improve running time for a static problem. 

Rules can be broken if it serves a higher purpose. For example, often one has to solve enumeration problems in order to solving an optimization problem.

Polylog factors are often ignored if it is $\log^c n$ for some large $c$.
Polylog factors are ignored if the algorithm is already more than quadratic time. 

Problem restricted to certain graph classes are discussed. In particular, bounded tree-width graphs. Mainly for tree-width $2$ graphs. Sometimes, grid graphs and planar graphs will be covered.

## Notes

If the problem uses notion you never seen before, it is probably recorded in the glossary. 
The output is currently posted on [AlgoRange](https://algorange.com).

## Assumptions and Notations

For graphs, $n$ is always the number of vertices and $m$ is the number of edges. 
When we use $m$ in running time, we mean $m+n$, since it is rare when $m=o(n)$. 

## Ambitious updates

There are many problems are basically the same, but under different restrictions.
For example, the shortest path tree problem.
It be interesting to capture it, so instead of having a problem, we have a generator for problems. Similar to the [scheduling problem notation](https://en.wikipedia.org/wiki/Notation_for_theoretic_scheduling_problems).

Isolate the input size parameters and the running time. 
