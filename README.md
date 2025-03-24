# CentraleSupélec AI Automated Planning Course

This repository contains course projects focusing on automated planning using STRIPS and PDDL formalisms. Each project demonstrates different planning concepts and problem-solving techniques.

## STRIPS and PDDL Overview

### STRIPS Planning

STRIPS (Stanford Research Institute Problem Solver) is a formal language for expressing automated planning problems. The key components of STRIPS are:

- **States**: Represented by sets of logical predicates
- **Actions**: Specified by preconditions and effects
- **Goals**: Conditions that must be satisfied by a goal state
- **Initial State**: The starting state of the planning problem

### PDDL (Planning Domain Definition Language)

PDDL extends STRIPS and provides a standardized way to represent planning problems:

- **Types**: Define categories of objects
- **Predicates**: Define relations between objects
- **Actions**: Define state transitions with parameters, preconditions, and effects
- **Requirements**: Specify language features needed for the domain
- **Domain/Problem Separation**: Enables reuse of domain definitions across different problem instances

## Projects

### Hamiltonian Cycle

The main project in this repository models and solves the Hamiltonian Cycle problem using PDDL planning.

#### Problem Description

A Hamiltonian cycle is a path in an undirected graph that visits each vertex exactly once and returns to the starting vertex. This problem is NP-complete, making it an excellent test case for planning algorithms.

#### PDDL Model

The Hamiltonian Cycle PDDL model includes:

- **Types**: `vertex` and `count`
- **Predicates**:
  - `(connected ?v1 ?v2)`: Edge between vertices
  - `(visited ?v)`: Vertex has been visited
  - `(current ?v)`: Current position
  - `(start ?v)`: Starting vertex
  - `(path-length ?n)`: Number of vertices visited
- **Actions**:
  - `select-start`: Choose a starting vertex
  - `move-to-next`: Move to an unvisited adjacent vertex
  - `complete-cycle`: Return to the starting vertex

#### Graph Generator

The repository includes a Python script (`hamiltonian_cycle.py`) that:

- Generates random connected graphs
- Creates corresponding PDDL problem files
- Runs the FF planner to find solutions
- Visualizes both the original graph and solution

#### Batch Generation

Use the shell script to generate multiple problem instances:

```bash
./generate_problems.sh
```

This creates problems with varying vertex counts and edge probabilities, naming each file according to its parameters.

### Turing Machine

This project models a Turing Machine using PDDL, demonstrating how to represent state transitions and tape manipulations in a planning context.

#### Turing Machine: Goal

To model a computational process where a machine traverses a tape, reads and writes symbols based on its current state and the symbol it reads, and then moves the read/write head.

### Tower of Hanoi

A classic problem modeled in PDDL, where disks of different sizes must be moved between pegs following specific rules.

#### Tower of Hanoi: Goal

To move a stack of disks from one peg to another, one at a time, never placing a larger disk on top of a smaller one.

### Blocks World

A standard planning domain involving stacking and unstacking blocks to achieve a desired configuration.

#### Blocks world: Goal

To rearrange blocks from an initial configuration to a goal configuration using four operators: pick-up, put-down, stack, and unstack.

## Running the Hamiltonian Cycle Generator

### Prerequisites

- Python 3.x
- NetworkX and Matplotlib libraries
- FF Planner

### Usage

```bash
python hamiltonian_cycle.py --vertices <num_vertices> --edge-prob <probability>
```

### Parameters

- `--vertices`: Number of vertices in the graph
- `--edge-prob`: Probability of an edge between any two vertices
- `--domain`: Domain file path (default: domain.pddl)
- `--problem`: Output problem file path (default: problem.pddl)

### Output

- PDDL problem file
- Visualization of the original graph
- Visualization of the solution (if found)
- Planner output with solution steps
