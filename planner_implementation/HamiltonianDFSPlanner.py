import argparse as ap
import logging

import pddl
import pddl.logic
import pddl.logic.base
from pddl import parse_domain, parse_problem

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s -  %(levelname)s - %(message)s",
    filename="planner.log",
    filemode="w",
)
logger = logging.getLogger(__name__)


class State:
    def __init__(self, atoms, plan=None):
        self.atoms = set(atoms)
        self.plan = plan or []

    def satisfies(self, goal):
        function_name = "satisfies"
        logger.debug(
            f"{self.__class__.__name__}.{function_name}: Checking if state satisfies goal: {goal}"
        )
        if isinstance(goal, pddl.logic.base.And):
            logger.debug(
                f"{self.__class__.__name__}.{function_name}: Goal is a conjunction"
            )
            logger.debug(
                f"{self.__class__.__name__}.{function_name}: State atoms: {self.atoms}"
            )
            logger.debug(
                f"{self.__class__.__name__}.{function_name}: Goal operands: {goal.operands}"
            )
            return all(atom in self.atoms for atom in goal.operands)

        for atom in self.atoms:
            if isinstance(atom, pddl.logic.Predicate) and atom.name == goal.name:
                # Check if all arguments match
                if len(atom.terms) != len(goal.terms):
                    logger.debug(
                        f"{self.__class__.__name__}.{function_name}: Atom {atom} and goal {goal} have different arities"
                    )
                    continue
                for arg1, arg2 in zip(atom.terms, goal.terms):
                    if arg1.name.replace("?", "") != arg2.name.replace("?", ""):
                        logger.debug(
                            f"{self.__class__.__name__}.{function_name}: Arguments {arg1} and {arg2} do not match in atom {atom}"
                        )
                        break
                else:
                    logger.debug(
                        f"{self.__class__.__name__}.{function_name}: Goal {goal} satisfied by atom {atom}"
                    )
                    return True
        logger.debug(
            f"{self.__class__.__name__}.{function_name}: Goal {goal} not satisfied by state {self.atoms}"
        )
        return False

    def __hash__(self):
        return hash(frozenset(self.atoms))

    def __eq__(self, other):
        for atom in self.atoms:
            if atom not in other.atoms:
                return False
        for atom in other.atoms:
            if atom not in self.atoms:
                return False
        return True

    def __str__(self):
        return f"State(atoms={self.atoms}, plan={self.plan})"


class Planner:
    def __init__(self, domain, problem):
        self.domain = domain
        self.problem = problem
        self.initial_state = State(problem.init)
        self.goal = problem.goal
        self.actions = domain.actions
        self.visited_states = set()
        self.solution = None

    def plan(self):
        function_name = "plan"
        logger.info(
            f"{self.__class__.__name__}.{function_name}: Starting planning process"
        )
        logger.info(
            f"{self.__class__.__name__}.{function_name}: Domain: {self.domain.name}"
        )
        logger.info(
            f"{self.__class__.__name__}.{function_name}: Problem: {self.problem.name}"
        )
        logger.info(
            f"{self.__class__.__name__}.{function_name}: Initial state: {self.initial_state}"
        )
        logger.info(f"{self.__class__.__name__}.{function_name}: Goal: {self.goal}")
        logger.info(
            f"{self.__class__.__name__}.{function_name}: Number of actions: {len(self.actions)}"
        )
        logger.info(
            f"{self.__class__.__name__}.{function_name}: Number of objects: {len(self.problem.objects)}"
        )
        logger.info(
            f"{self.__class__.__name__}.{function_name}: Number of initial atoms: {len(self.initial_state.atoms)}"
        )
        logger.info(f"{self.__class__.__name__}.{function_name}: Starting DFS")
        logger.info("=====================================")
        logger.info("=====================================")
        if self.dfs(self.initial_state):
            return self.solution
        return None

    def dfs(self, state: State):
        function_name = "dfs"
        logger.debug(
            f"{self.__class__.__name__}.{function_name}: Current state: {state}"
        )
        logger.debug(
            f"{self.__class__.__name__}.{function_name}: checking if state satisfies goal: {self.goal}"
        )
        if state.satisfies(self.goal):
            self.solution = state.plan
            logger.info(
                f"{self.__class__.__name__}.{function_name}: Goal state reached! Solution found."
            )
            return True
        self.visited_states.add(state)
        logger.debug(
            f"{self.__class__.__name__}.{function_name}: Exploring state with {len(state.atoms)} atoms, visited states: {len(self.visited_states)}"
        )
        for action in self.actions:
            logger.debug("=====================================")
            logger.debug(
                f"{self.__class__.__name__}.{function_name}: Considering action: {action.name}"
            )
            for binding in self.get_applicable_bindings(action, state):
                logger.info(
                    f"{self.__class__.__name__}.{function_name}: Applying action {action.name} with binding {binding}"
                )
                new_state = self.apply_action(state, action, binding)
                if new_state in self.visited_states:
                    logger.debug(
                        f"{self.__class__.__name__}.{function_name}: State already visited, skipping"
                    )
                    continue
                new_state.plan.append((action.name, binding))
                if self.dfs(new_state):
                    return True
        logger.debug(
            f"{self.__class__.__name__}.{function_name}: No solution found from this state, backtracking"
        )
        logger.debug("-------------------------------------")
        return False

    def get_applicable_bindings(self, action, state):
        function_name = "get_applicable_bindings"
        logger.debug(
            f"{self.__class__.__name__}.{function_name}: Checking if action {action.name} is applicable"
        )
        logger.debug(
            f"{self.__class__.__name__}.{function_name}: Action parameters: {action.parameters}"
        )
        logger.debug(
            f"{self.__class__.__name__}.{function_name}: Action precondition: {action.precondition}"
        )
        logger.debug(
            f"{self.__class__.__name__}.{function_name}: State atoms: {state.atoms}"
        )
        logger.debug(
            f"{self.__class__.__name__}.{function_name}: State atoms: {state.atoms}"
        )

        # If action has no parameters, just check the precondition
        if not action.parameters:
            if self.holds(action.precondition, state):
                return [{}]
            return []

        # Get all objects from the problem
        objects = self.problem.objects
        logger.debug(
            f"{self.__class__.__name__}.{function_name}: Objects in the problem: {objects}"
        )

        # Generate all possible bindings
        all_bindings = self._generate_bindings(action.parameters, objects)
        logger.debug(
            f"{self.__class__.__name__}.{function_name}: Generated {len(all_bindings)} possible bindings"
        )
        logger.debug(
            f"{self.__class__.__name__}.{function_name}: Bindings: {all_bindings}"
        )

        # Filter bindings where preconditions hold
        valid_bindings = []
        for binding in all_bindings:
            # Apply binding to precondition
            grounded_precond = self._substitute(action.precondition, binding)
            logger.debug(
                f"{self.__class__.__name__}.{function_name}: Grounded precondition: {grounded_precond}"
            )
            if self.holds(grounded_precond, state):
                logger.debug(
                    f"{self.__class__.__name__}.{function_name}: Found valid binding: {binding}"
                )
                valid_bindings.append(binding)

        logger.debug(
            f"{self.__class__.__name__}.{function_name}: Found {len(valid_bindings)} valid bindings"
        )
        return valid_bindings

    def _generate_bindings(self, parameters, objects):
        function_name = "_generate_bindings"
        """Generate all possible bindings for parameters"""
        if not parameters:
            return [{}]

        # Get possible values for each parameter based on its type
        param_values = {}
        for param in parameters:
            logger.debug(
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
        function_name = "_substitute"
        """Apply binding to a formula, handling Variables vs Constants correctly."""
        if isinstance(formula, pddl.logic.base.And):
            return pddl.logic.base.And(
                *[self._substitute(op, binding) for op in formula.operands]
            )
        elif isinstance(formula, pddl.logic.base.Not):
            return pddl.logic.base.Not(self._substitute(formula.argument, binding))
        elif isinstance(formula, pddl.logic.Predicate):
            logger.debug(
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
        function_name = "holds"
        """Check if a formula holds in the given state"""
        if isinstance(formula, pddl.logic.base.And):
            result = all(self.holds(op, state) for op in formula.operands)
            logger.debug(
                f"{self.__class__.__name__}.{function_name}: AND formula evaluated to {result}"
            )
            return result
        elif isinstance(formula, pddl.logic.base.Not):
            result = not self.holds(formula.argument, state)
            logger.debug(
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
        function_name = "apply_action"
        logger.debug(
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
                        logger.error(
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
                            logger.debug(
                                f"{self.__class__.__name__}.{function_name}: Removing atom {atom}"
                            )
                            new_atoms.remove(atom)
                            break
                else:
                    logger.debug(
                        f"{self.__class__.__name__}.{function_name}: Adding atom {eff}"
                    )
                    new_atoms.add(eff)
        elif isinstance(grounded_effect, pddl.logic.base.Not):
            # Ensure grounded_effect.argument is a Predicate
            atom_to_remove = grounded_effect.argument
            if not isinstance(atom_to_remove, pddl.logic.Predicate):
                logger.error(
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
                        logger.debug(
                            f"{self.__class__.__name__}.{function_name}: Removing atom {atom}"
                        )
                        new_atoms.remove(atom)
                        break
        else:
            logger.debug(
                f"{self.__class__.__name__}.{function_name}: Adding atom {grounded_effect}"
            )
            new_atoms.add(grounded_effect)

        logger.debug(
            f"{self.__class__.__name__}.{function_name}: New state has {len(new_atoms)} atoms"
        )
        logger.debug(
            f"{self.__class__.__name__}.{function_name}: Old state atoms: {state.atoms}"
        )
        logger.debug(
            f"{self.__class__.__name__}.{function_name}: New state atoms: {new_atoms}"
        )
        return State(new_atoms, plan=list(state.plan))


if __name__ == "__main__":
    apr = ap.ArgumentParser(
        description="Hamiltonian Cycle Planner using DFS",
        formatter_class=ap.ArgumentDefaultsHelpFormatter,
    )
    apr.add_argument(
        "-d",
        "--domain",
        type=str,
        help="Path to the domain file",
    )
    apr.add_argument(
        "-p",
        "--problem",
        type=str,
        help="Path to the problem file",
    )
    apr.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )
    args = apr.parse_args()
    if args.verbose:
        logger.setLevel(logging.DEBUG)
        logger.info("Verbose logging enabled")
    else:
        logger.setLevel(logging.INFO)
        logger.info("Verbose logging disabled")
    # Example domain and problem files
    # 1. Domain file
    domain_file = args.domain
    problem_file = args.problem

    logger.info("Starting planning process")
    logger.info(f"Domain file: {domain_file}")
    logger.info(f"Problem file: {problem_file}")

    domain = parse_domain(domain_file)
    problem = parse_problem(problem_file)

    logger.info(f"Domain parsed: {domain.name}")
    logger.info(f"Problem parsed: {problem.name}")

    planner = Planner(domain, problem)
    logger.info("Starting planning")
    plan = planner.plan()
    if plan:
        logger.info("Plan found!")
        for i, step in enumerate(plan):
            logger.info(f"Step {i + 1}: {step}")
            print(step)
    else:
        logger.warning("No plan found.")
        print("No plan found.")
