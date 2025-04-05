# Automated Planning with Depth-First Search (DFS)

This project implements an automated planning system using a Depth-First Search (DFS) algorithm. The system is designed to solve planning problems defined in the **Planning Domain Definition Language (PDDL)**. The goal is to find a sequence of actions that transitions an initial state to a goal state.

## Overview

Automated planning is a branch of artificial intelligence that focuses on finding a sequence of actions to achieve a specific goal. This project uses a DFS-based approach to explore the state space of a planning problem.

### Key Components

1. **Planner**:
   - The `Planner` class is the core of the system. It implements the DFS algorithm to explore the state space and find a solution.
   - It takes a PDDL domain and problem as input and attempts to find a sequence of actions that satisfies the goal condition.

2. **State**:
   - The `State` class represents a state in the planning problem. A state consists of a set of atoms (facts) and an optional plan (sequence of actions leading to the state).
   - It provides methods to check if a state satisfies a goal condition.

3. **PDDL Parsing**:
   - The system uses PDDL parsers to read and interpret domain and problem files. These files define the actions, objects, initial state, and goal state.

4. **Logging**:
   - The system uses Python's `logging` module to provide detailed logs of the planning process, including debugging information.

## Algorithm Details

The algorithm uses **Depth-First Search (DFS)** to explore the state space. Here's how it works:

1. **Initialization**:
   - The planner initializes with the domain, problem, and initial state.
   - The goal condition and available actions are extracted from the problem and domain.

2. **DFS Exploration**:
   - Starting from the initial state, the planner recursively explores the state space.
   - For each state, it checks if the goal condition is satisfied. If so, the solution (sequence of actions) is returned.

3. **Action Application**:
   - For each action, the planner generates all possible bindings of action parameters to objects in the problem.
   - It applies the action to the current state, producing a new state.

4. **State Pruning**:
   - The planner keeps track of visited states to avoid revisiting them, reducing redundant computations.

5. **Backtracking**:
   - If no solution is found from a state, the planner backtracks to explore other branches of the state space.

6. **Solution**:
   - If a sequence of actions is found that transitions the initial state to the goal state, it is returned as the solution. Otherwise, the planner reports that no solution was found.

## Input and Output

### Input

The system requires two files as input:

1. **Domain File**: Defines the actions, predicates, and types in the planning problem.
2. **Problem File**: Defines the objects, initial state, and goal state.

### Output

If a solution is found, the planner outputs:

- The sequence of actions in the plan.
- A `.pddl.plan` file containing the plan.

If no solution is found, the planner reports that no plan was found.

## Example Usage

1. Prepare the domain and problem files in PDDL format.
2. Run the planner using the following command:

   ```bash
   python dfs_planner.py -d path/to/domain.pddl -p path/to/problem.pddl
   ```

3. Use the `-v` flag for verbose logging:

   ```bash
   python dfs_planner.py -d path/to/domain.pddl -p path/to/problem.pddl -v
   ```

### Example Output

If a plan is found, the output will look like this:

```bash
( select-start v5 n0 n1 )
( move-to-next v5 v1 n1 n2 )
( move-to-next v1 v3 n2 n3 )
( move-to-next v3 v4 n3 n4 )
( move-to-next v4 v2 n4 n5 )
( complete-cycle v2 v5 n5 )

```

The plan will also be saved to a file named `<problem_name>.pddl.plan`.

## Logging

The system logs the planning process to a file named `planner.log`. The log includes:

- Information about the domain and problem.
- Details of the DFS exploration.
- Debugging information for actions, states, and bindings.

## Limitations

- The DFS algorithm is not optimal and may not find the shortest plan.
- The algorithm may not scale well for large state spaces due to its exhaustive nature.

## Future Improvements

- Implement more efficient search algorithms like A* or breadth-first search.
- Add support for heuristic functions to guide the search.
- Improve scalability for larger and more complex planning problems.

## Conclusion

This project demonstrates the use of DFS for automated planning in PDDL environments. While simple, it provides a foundation for exploring more advanced planning techniques.
