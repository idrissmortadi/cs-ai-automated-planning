"""
state.py

This module defines the State class, which represents a state in the planning
problem. A state consists of a set of atoms (facts) and optionally a plan,
which is a sequence of actions that led to the state.
"""

import logging

import pddl


class State:
    """
    Represents a state in the planning problem.

    Attributes:
        atoms (set): A set of atoms (facts) that define the state.
        plan (list): A sequence of actions that led to this state.
    """

    def __init__(self, atoms, plan=None, logger=None):
        """
        Initialize a State with a set of atoms and an optional plan.

        Args:
            atoms (set): A set of atoms (facts) that define the state.
            plan (list, optional): A sequence of actions that led to this state. Defaults to an empty list.
        """
        self.atoms = set(atoms)
        self.plan = plan or []
        self.logger = logger or logging.getLogger(__name__)

    def satisfies(self, goal):
        """
        Check if the state satisfies the given goal condition.

        Args:
            goal (Condition): The goal condition to check.

        Returns:
            bool: True if the state satisfies the goal, False otherwise.
        """
        function_name = "satisfies"
        self.logger.debug(
            f"{self.__class__.__name__}.{function_name}: Checking if state satisfies goal: {goal}"
        )
        if isinstance(goal, pddl.logic.base.And):
            self.logger.debug(
                f"{self.__class__.__name__}.{function_name}: Goal is a conjunction"
            )
            self.logger.debug(
                f"{self.__class__.__name__}.{function_name}: State atoms: {self.atoms}"
            )
            self.logger.debug(
                f"{self.__class__.__name__}.{function_name}: Goal operands: {goal.operands}"
            )
            return all(atom in self.atoms for atom in goal.operands)

        for atom in self.atoms:
            if isinstance(atom, pddl.logic.Predicate) and atom.name == goal.name:
                # Check if all arguments match
                if len(atom.terms) != len(goal.terms):
                    self.logger.debug(
                        f"{self.__class__.__name__}.{function_name}: Atom {atom} and goal {goal} have different arities"
                    )
                    continue
                for arg1, arg2 in zip(atom.terms, goal.terms):
                    if arg1.name.replace("?", "") != arg2.name.replace("?", ""):
                        self.logger.debug(
                            f"{self.__class__.__name__}.{function_name}: Arguments {arg1} and {arg2} do not match in atom {atom}"
                        )
                        break
                else:
                    self.logger.debug(
                        f"{self.__class__.__name__}.{function_name}: Goal {goal} satisfied by atom {atom}"
                    )
                    return True
        self.logger.debug(
            f"{self.__class__.__name__}.{function_name}: Goal {goal} not satisfied by state {self.atoms}"
        )
        return False

    def __hash__(self):
        """
        Compute a hash value for the state based on its atoms.

        Returns:
            int: The hash value of the state.
        """
        return hash(frozenset(self.atoms))

    def __eq__(self, other):
        """
        Check if this state is equal to another state.

        Args:
            other (State): The state to compare with.

        Returns:
            bool: True if the states are equal, False otherwise.
        """
        for atom in self.atoms:
            if atom not in other.atoms:
                return False
        for atom in other.atoms:
            if atom not in self.atoms:
                return False
        return True

    def __str__(self):
        """
        Return a string representation of the state.

        Returns:
            str: A string representation of the state.
        """
        return f"State(atoms={self.atoms}, plan={self.plan})"
