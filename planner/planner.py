"""
planner.py

This module defines the Planner class, which implements a depth-first search (DFS)
algorithm for automated planning in a PDDL (Planning Domain Definition Language)
environment. The Planner class takes a domain and problem as input and attempts
to find a sequence of actions that transitions the initial state to the goal state.
"""

import logging

import pddl
from state import State


class Planner:
    """
    A planner that uses depth-first search (DFS) to solve planning problems
    defined in PDDL. The planner explores the state space to find a sequence
    of actions that satisfies the goal condition.

    Attributes:
        domain (Domain): The PDDL domain containing actions and predicates.
        problem (Problem): The PDDL problem containing the initial state, goal, and objects.
        initial_state (State): The initial state of the problem.
        goal (Condition): The goal condition to be satisfied.
        actions (list): A list of actions defined in the domain.
        visited_states (set): A set of states that have already been visited.
        solution (list): The sequence of actions that solves the problem, if found.
        logger (Logger): A logger for debugging and informational messages.
    """

    def __init__(self, domain, problem, logger=None):
        """
        Initialize the Planner with a domain, problem, and optional logger.

        Args:
            domain (Domain): The PDDL domain containing actions and predicates.
            problem (Problem): The PDDL problem containing the initial state, goal, and objects.
            logger (Logger, optional): A logger for debugging and informational messages. Defaults to None.
        """
        self.domain = domain
        self.problem = problem
        self.initial_state = State(problem.init)
        self.goal = problem.goal
        self.actions = domain.actions
        self.visited_states = set()
        self.solution = None
        self.logger = logger or logging.getLogger(__name__)

    def plan(self):
        """
        Perform the planning process using depth-first search (DFS).

        Logs the planning process and attempts to find a solution that transitions
        the initial state to the goal state.

        Returns:
            list: A sequence of actions that solves the problem, or None if no solution is found.
        """
        function_name = "plan"
        self.logger.info(
            f"{self.__class__.__name__}.{function_name}: Starting planning process"
        )
        self.logger.info(
            f"{self.__class__.__name__}.{function_name}: Domain: {self.domain.name}"
        )
        self.logger.info(
            f"{self.__class__.__name__}.{function_name}: Problem: {self.problem.name}"
        )
        self.logger.info(
            f"{self.__class__.__name__}.{function_name}: Initial state: {self.initial_state}"
        )
        self.logger.info(
            f"{self.__class__.__name__}.{function_name}: Goal: {self.goal}"
        )
        self.logger.info(
            f"{self.__class__.__name__}.{function_name}: Number of actions: {len(self.actions)}"
        )
        self.logger.info(
            f"{self.__class__.__name__}.{function_name}: Number of objects: {len(self.problem.objects)}"
        )
        self.logger.info(
            f"{self.__class__.__name__}.{function_name}: Number of initial atoms: {len(self.initial_state.atoms)}"
        )
        self.logger.info(f"{self.__class__.__name__}.{function_name}: Starting DFS")
        self.logger.info("=====================================")
        self.logger.info("=====================================")
        if self.dfs(self.initial_state):
            return self.solution
        return None

    def dfs(self, state: State):
        """
        Perform a depth-first search (DFS) from the given state.

        Args:
            state (State): The current state to explore.

        Returns:
            bool: True if a solution is found, False otherwise.
        """
        function_name = "dfs"
        self.logger.debug(
            f"{self.__class__.__name__}.{function_name}: Current state: {state}"
        )
        self.logger.debug(
            f"{self.__class__.__name__}.{function_name}: checking if state satisfies goal: {self.goal}"
        )
        if state.satisfies(self.goal):
            self.solution = state.plan
            self.logger.info(
                f"{self.__class__.__name__}.{function_name}: Goal state reached! Solution found."
            )
            return True
        self.visited_states.add(state)
        self.logger.debug(
            f"{self.__class__.__name__}.{function_name}: Exploring state with {len(state.atoms)} atoms, visited states: {len(self.visited_states)}"
        )
        for action in self.actions:
            self.logger.debug("=====================================")
            self.logger.debug(
                f"{self.__class__.__name__}.{function_name}: Considering action: {action.name}"
            )
            for binding in self.get_applicable_bindings(action, state):
                self.logger.info(
                    f"{self.__class__.__name__}.{function_name}: Applying action {action.name} with binding {binding}"
                )
                new_state = self.apply_action(state, action, binding)
                if new_state in self.visited_states:
                    self.logger.debug(
                        f"{self.__class__.__name__}.{function_name}: State already visited, skipping"
                    )
                    continue
                new_state.plan.append((action.name, binding))
                if self.dfs(new_state):
                    return True
        self.logger.debug(
            f"{self.__class__.__name__}.{function_name}: No solution found from this state, backtracking"
        )
        self.logger.debug("-------------------------------------")
        return False

    def get_applicable_bindings(self, action, state):
        """
        Get all valid bindings for an action's parameters in the given state.

        Args:
            action (Action): The action to check.
            state (State): The current state.

        Returns:
            list: A list of valid bindings (dictionaries) for the action's parameters.
        """
        function_name = "get_applicable_bindings"
        self.logger.debug(
            f"{self.__class__.__name__}.{function_name}: Checking if action {action.name} is applicable"
        )
        self.logger.debug(
            f"{self.__class__.__name__}.{function_name}: Action parameters: {action.parameters}"
        )
        self.logger.debug(
            f"{self.__class__.__name__}.{function_name}: Action precondition: {action.precondition}"
        )
        self.logger.debug(
            f"{self.__class__.__name__}.{function_name}: State atoms: {state.atoms}"
        )
        self.logger.debug(
            f"{self.__class__.__name__}.{function_name}: State atoms: {state.atoms}"
        )

        # If action has no parameters, just check the precondition
        if not action.parameters:
            if self.holds(action.precondition, state):
                return [{}]
            return []

        # Get all objects from the problem
        objects = self.problem.objects
        self.logger.debug(
            f"{self.__class__.__name__}.{function_name}: Objects in the problem: {objects}"
        )

        # Generate all possible bindings
        all_bindings = self._generate_bindings(action.parameters, objects)
        self.logger.debug(
            f"{self.__class__.__name__}.{function_name}: Generated {len(all_bindings)} possible bindings"
        )
        self.logger.debug(
            f"{self.__class__.__name__}.{function_name}: Bindings: {all_bindings}"
        )

        # Filter bindings where preconditions hold
        valid_bindings = []
        for binding in all_bindings:
            # Apply binding to precondition
            grounded_precond = self._substitute(action.precondition, binding)
            self.logger.debug(
                f"{self.__class__.__name__}.{function_name}: Grounded precondition: {grounded_precond}"
            )
            if self.holds(grounded_precond, state):
                self.logger.debug(
                    f"{self.__class__.__name__}.{function_name}: Found valid binding: {binding}"
                )
                valid_bindings.append(binding)

        self.logger.debug(
            f"{self.__class__.__name__}.{function_name}: Found {len(valid_bindings)} valid bindings"
        )
        return valid_bindings

    def _generate_bindings(self, parameters, objects):
        """
        Generate all possible bindings for the given parameters using the available objects.

        Args:
            parameters (list): A list of parameters to bind.
            objects (list): A list of objects available in the problem.

        Returns:
            list: A list of all possible bindings (dictionaries).
        """
        function_name = "_generate_bindings"
        """Generate all possible bindings for parameters"""
        if not parameters:
            return [{}]

        # Get possible values for each parameter based on its type
        param_values = {}
        for param in parameters:
            self.logger.debug(
                f"{self.__class__.__name__}.{function_name}: Generating values for parameter {param.name}"
            )
            param_type = param.type_tags
            param_values[param.name] = [
                obj.name for obj in objects if obj.type_tags == param_type
            ]

        # Generate all combinations
        return self._generate_binding_combinations(
            {}, param_values, list(param_values.keys())
        )

    def _generate_binding_combinations(
        self, current_binding, param_values, remaining_params
    ):
        """
        Recursively generate all combinations of bindings for parameters.

        Args:
            current_binding (dict): The current partial binding.
            param_values (dict): A dictionary mapping parameters to their possible values.
            remaining_params (list): A list of parameters yet to be bound.

        Returns:
            list: A list of all possible bindings (dictionaries).
        """
        # function_name = "_generate_binding_combinations"
        """Recursively generate all binding combinations"""
        if not remaining_params:
            return [current_binding]

        bindings = []
        current_param = remaining_params[0]
        for value in param_values[current_param]:
            new_binding = current_binding.copy()
            new_binding[current_param] = value
            bindings.extend(
                self._generate_binding_combinations(
                    new_binding, param_values, remaining_params[1:]
                )
            )
        return bindings

    def _substitute(self, formula, binding):
        """
        Apply a binding to a formula, replacing variables with constants.

        Args:
            formula (Formula): The formula to substitute into.
            binding (dict): A dictionary mapping variable names to object names.

        Returns:
            Formula: The grounded formula with variables replaced by constants.
        """
        function_name = "_substitute"
        """Apply binding to a formula, handling Variables vs Constants correctly."""
        if isinstance(formula, pddl.logic.base.And):
            return pddl.logic.base.And(
                *[self._substitute(op, binding) for op in formula.operands]
            )
        elif isinstance(formula, pddl.logic.base.Not):
            return pddl.logic.base.Not(self._substitute(formula.argument, binding))
        elif isinstance(formula, pddl.logic.Predicate):
            self.logger.debug(
                f"{self.__class__.__name__}.{function_name}: Substituting in predicate {formula.name}"
            )
            new_args = []
            for arg in formula.terms:
                if isinstance(arg, pddl.logic.terms.Variable):
                    # Look up the binding
                    var_key = arg.name
                    new_value = binding.get(var_key, var_key)
                    # Create a Constant for bound values (concrete objects)
                    new_args.append(pddl.logic.terms.Constant(new_value))
                else:
                    new_args.append(arg)
            return formula(*new_args)
        return formula

    def holds(self, formula, state):
        """
        Check if a formula holds in the given state.

        Args:
            formula (Formula): The formula to evaluate.
            state (State): The current state.

        Returns:
            bool: True if the formula holds, False otherwise.
        """
        function_name = "holds"
        """Check if a formula holds in the given state"""
        if isinstance(formula, pddl.logic.base.And):
            result = all(self.holds(op, state) for op in formula.operands)
            self.logger.debug(
                f"{self.__class__.__name__}.{function_name}: AND formula evaluated to {result}"
            )
            return result
        elif isinstance(formula, pddl.logic.base.Not):
            result = not self.holds(formula.argument, state)
            self.logger.debug(
                f"{self.__class__.__name__}.{function_name}: NOT formula evaluated to {result}"
            )
            return result

        for atom in state.atoms:
            if isinstance(atom, pddl.logic.Predicate) and atom.name == formula.name:
                # Check if all arguments match
                if len(atom.terms) != len(formula.terms):
                    continue
                # Match using exact method as in State.satisfies
                match = True
                for arg1, arg2 in zip(atom.terms, formula.terms):
                    if arg1.name.replace("?", "") != arg2.name.replace("?", ""):
                        match = False
                        break
                if match:
                    return True
        return False

    def apply_action(self, state, action, binding):
        """
        Apply an action with a given binding to a state, producing a new state.

        Args:
            state (State): The current state.
            action (Action): The action to apply.
            binding (dict): A dictionary mapping action parameters to object names.

        Returns:
            State: The new state resulting from applying the action.
        """
        function_name = "apply_action"
        self.logger.debug(
            f"{self.__class__.__name__}.{function_name}: Applying action {action.name} with binding {binding}"
        )
        new_atoms = set(state.atoms)

        # Apply binding to effect
        grounded_effect = self._substitute(action.effect, binding)

        if isinstance(grounded_effect, pddl.logic.base.And):
            for eff in grounded_effect.operands:
                if isinstance(eff, pddl.logic.base.Not):
                    # Ensure eff.argument is a Predicate
                    atom_to_remove = eff.argument
                    if not isinstance(atom_to_remove, pddl.logic.Predicate):
                        self.logger.error(
                            f"{self.__class__.__name__}.{function_name}: Expected Predicate, got {type(atom_to_remove)}"
                        )
                        continue
                    for atom in list(new_atoms):
                        if (
                            isinstance(atom, pddl.logic.Predicate)
                            and atom.name == atom_to_remove.name
                            and len(atom.terms) == len(atom_to_remove.terms)
                            and all(
                                a1.name.replace("?", "") == a2.name.replace("?", "")
                                for a1, a2 in zip(atom.terms, atom_to_remove.terms)
                            )
                        ):
                            self.logger.debug(
                                f"{self.__class__.__name__}.{function_name}: Removing atom {atom}"
                            )
                            new_atoms.remove(atom)
                            break
                else:
                    self.logger.debug(
                        f"{self.__class__.__name__}.{function_name}: Adding atom {eff}"
                    )
                    new_atoms.add(eff)
        elif isinstance(grounded_effect, pddl.logic.base.Not):
            # Ensure grounded_effect.argument is a Predicate
            atom_to_remove = grounded_effect.argument
            if not isinstance(atom_to_remove, pddl.logic.Predicate):
                self.logger.error(
                    f"{self.__class__.__name__}.{function_name}: Expected Predicate, got {type(atom_to_remove)}"
                )
            else:
                for atom in list(new_atoms):
                    if (
                        isinstance(atom, pddl.logic.Predicate)
                        and atom.name == atom_to_remove.name
                        and len(atom.terms) == len(atom_to_remove.terms)
                        and all(
                            a1.name.replace("?", "") == a2.name.replace("?", "")
                            for a1, a2 in zip(atom.terms, atom_to_remove.terms)
                        )
                    ):
                        self.logger.debug(
                            f"{self.__class__.__name__}.{function_name}: Removing atom {atom}"
                        )
                        new_atoms.remove(atom)
                        break
        else:
            self.logger.debug(
                f"{self.__class__.__name__}.{function_name}: Adding atom {grounded_effect}"
            )
            new_atoms.add(grounded_effect)

        self.logger.debug(
            f"{self.__class__.__name__}.{function_name}: New state has {len(new_atoms)} atoms"
        )
        self.logger.debug(
            f"{self.__class__.__name__}.{function_name}: Old state atoms: {state.atoms}"
        )
        self.logger.debug(
            f"{self.__class__.__name__}.{function_name}: New state atoms: {new_atoms}"
        )
        return State(new_atoms, plan=list(state.plan))
