import os
import tempfile

import pddl.logic.base as logic
import pytest
from HamiltonianDFSPlanner import Planner, State
from pddl import parse_domain, parse_problem
from pddl.logic.predicates import Predicate
from pddl.logic.terms import Constant, Variable


# Helper function to create test domain file
def create_domain_file():
    domain_str = """
    (define (domain test-domain)
      (:requirements :strips)
      (:predicates 
        (at ?x)
        (connected ?x ?y)
        (visited ?x)
      )
      
      (:action move
        :parameters (?from ?to)
        :precondition (and (at ?from) (connected ?from ?to))
        :effect (and (not (at ?from)) (at ?to) (visited ?to))
      )
    )
    """
    fd, path = tempfile.mkstemp(suffix=".pddl")
    with os.fdopen(fd, "w") as f:
        f.write(domain_str)
    return path


# Helper function to create test problem file
def create_problem_file():
    problem_str = """
    (define (problem test-problem)
      (:domain test-domain)
      (:objects n1 n2 n3)
      (:init
        (at n1)
        (connected n1 n2)
        (connected n2 n3)
        (connected n3 n1)
        (visited n1)
      )
      (:goal (and (at n1) (visited n1) (visited n2) (visited n3)))
    )
    """
    fd, path = tempfile.mkstemp(suffix=".pddl")
    with os.fdopen(fd, "w") as f:
        f.write(problem_str)
    return path


# Fixture to setup domain and problem
@pytest.fixture
def setup_planner():
    domain_file = create_domain_file()
    problem_file = create_problem_file()

    domain = parse_domain(domain_file)
    problem = parse_problem(problem_file)

    planner = Planner(domain, problem)

    # Cleanup temp files
    yield planner
    os.remove(domain_file)
    os.remove(problem_file)


# Test initialization
def test_init(setup_planner):
    planner = setup_planner
    assert planner.domain is not None
    assert planner.problem is not None
    assert isinstance(planner.initial_state, State)
    assert planner.goal is not None
    assert len(planner.actions) > 0
    assert isinstance(planner.visited_states, set)
    assert planner.solution is None


# Test State class
def test_state():
    # Create a simple state

    atom1 = Predicate("at", Variable("n1"))
    atom2 = Predicate("visited", Variable("n1"))
    state = State([atom1, atom2])

    # Test satisfies with a single atom
    assert state.satisfies(atom1)

    # Test satisfies with an AND formula
    goal = logic.And(atom1, atom2)
    assert state.satisfies(goal)

    # Test satisfies with missing atom
    atom3 = Predicate("visited", Variable("n2"))
    assert not state.satisfies(atom3)

    # Test hash and equality
    state2 = State([atom1, atom2])
    assert hash(state) == hash(state2)
    assert state == state2

    state3 = State([atom1])
    assert state != state3


# Test hold method
def test_holds(setup_planner):
    planner = setup_planner

    # Create atoms and a state
    atom1 = Predicate("at", Variable("n1"))
    atom2 = Predicate("visited", Variable("n1"))
    atom3 = Predicate("connected", Variable("n1"), Variable("n2"))
    state = State([atom1, atom2, atom3])

    # Test simple atom
    assert planner.holds(atom1, state)

    # Test atom not in state
    atom4 = Predicate("visited", Variable("n2"))
    assert not planner.holds(atom4, state)

    # Test AND formula
    and_formula = logic.And(atom1, atom2)
    assert planner.holds(and_formula, state)

    # Test AND formula with failing clause
    and_formula2 = logic.And(atom1, atom4)
    assert not planner.holds(and_formula2, state)

    # Test NOT formula
    not_formula = logic.Not(atom4)
    assert planner.holds(not_formula, state)

    # Test NOT formula that should fail
    not_formula2 = logic.Not(atom1)
    assert not planner.holds(not_formula2, state)


# Test _substitute method
def test_substitute(setup_planner):
    planner = setup_planner

    # Test substitution in a predicate
    pred = Predicate("at", Variable("x"))
    binding = {"x": "n1"}
    result = planner._substitute(pred, binding)
    assert result.name == "at"
    assert result.terms == (Constant("n1"),)

    # Test substitution in a more complex predicate
    pred2 = Predicate("connected", Variable("from"), Variable("to"))
    binding2 = {"from": "n1", "to": "n2"}
    result2 = planner._substitute(pred2, binding2)
    assert result2.name == "connected"
    assert result2.terms == (Constant("n1"), Constant("n2"))

    # Test substitution in AND formula
    and_formula = logic.And(
        Predicate("at", Variable("x")),
        Predicate("connected", Variable("x"), Variable("y")),
    )
    binding3 = {"x": "n1", "y": "n2"}
    result3 = planner._substitute(and_formula, binding3)
    assert isinstance(result3, logic.And)
    assert len(result3.operands) == 2
    assert result3.operands[0].terms == (Constant("n1"),)
    assert result3.operands[1].terms == (Constant("n1"), Constant("n2"))

    # Test substitution in NOT formula
    not_formula = logic.Not(Predicate("at", Variable("x")))
    result4 = planner._substitute(not_formula, binding)
    assert isinstance(result4, logic.Not)
    assert result4.argument.terms == (Constant("n1"),)


# Test _generate_bindings and _generate_binding_combinations methods
def test_generate_bindings(setup_planner):
    # TODO: Understand the purpose of this test
    planner = setup_planner

    # Create mock parameters and objects
    class MockParam:
        def __init__(self, name, type_tags):
            self.name = name
            self.type_tags = type_tags

    class MockObject:
        def __init__(self, name, type_tags):
            self.name = name
            self.type_tags = type_tags

    params = [MockParam("x", "node"), MockParam("y", "node")]

    objects = [
        MockObject("n1", "node"),
        MockObject("n2", "node"),
        MockObject("n3", "node"),
    ]

    # Test generating all bindings
    bindings = planner._generate_bindings(params, objects)
    assert len(bindings) == 9  # 3 options for ?x * 3 options for ?y

    # Check if all combinations are present
    expected_combinations = []
    for x in ["n1", "n2", "n3"]:
        for y in ["n1", "n2", "n3"]:
            expected_combinations.append({"x": x, "y": y})

    for combo in expected_combinations:
        assert combo in bindings

    # Test with empty parameters
    empty_bindings = planner._generate_bindings([], objects)
    assert len(empty_bindings) == 1
    assert empty_bindings[0] == {}


# Test get_applicable_bindings method
def test_get_applicable_bindings(setup_planner):
    planner = setup_planner

    # Create a test state
    at_n1 = Predicate("at", Variable("n1"))
    connected_n1_n2 = Predicate("connected", Variable("n1"), Variable("n2"))
    state = State([at_n1, connected_n1_n2])

    # Find the move action from the domain
    move_action = None
    for action in planner.domain.actions:
        if action.name == "move":
            move_action = action
            break

    assert move_action is not None

    # Test finding applicable bindings
    bindings = planner.get_applicable_bindings(move_action, state)

    # Since our state only has (at n1) and (connected n1 n2),
    # only the binding {from: n1, to: n2} should be applicable
    assert len(bindings) == 1
    assert "from" in bindings[0]
    assert "to" in bindings[0]
    assert bindings[0]["from"] == "n1"
    assert bindings[0]["to"] == "n2"

    # Test with a state where no bindings should be applicable
    state2 = State([connected_n1_n2])  # No 'at' predicate
    bindings2 = planner.get_applicable_bindings(move_action, state2)
    assert len(bindings2) == 0


# Test apply_action method
def test_apply_action(setup_planner):
    planner = setup_planner

    # Create atoms for test
    at_n1 = Predicate("at", Variable("n1"))
    connected_n1_n2 = Predicate("connected", Variable("n1"), Variable("n2"))
    visited_n1 = Predicate("visited", Variable("n1"))

    # Create a state
    state = State([at_n1, connected_n1_n2, visited_n1])

    # Find the move action (TODO: Find a better way to do this)
    move_action = None
    for action in planner.domain.actions:
        if action.name == "move":
            move_action = action
            break

    assert move_action is not None

    # Apply the action with binding
    binding = {"from": "n1", "to": "n2"}
    new_state = planner.apply_action(state, move_action, binding)

    # Check that 'at n1' was removed and 'at n2' was added
    assert Predicate("at", Constant("n1")) not in new_state.atoms
    assert Predicate("at", Constant("n2")) in new_state.atoms

    # Check that 'visited n2' was added
    assert Predicate("visited", Constant("n2")) in new_state.atoms

    # Check that other atoms were preserved
    assert connected_n1_n2 in new_state.atoms
    assert visited_n1 in new_state.atoms


# Test DFS method
def test_dfs(setup_planner):
    planner = setup_planner

    # The problem is solvable, so DFS should return True
    result = planner.dfs(planner.initial_state)
    assert result is True

    # Check that a solution was found
    assert planner.solution is not None
    assert len(planner.solution) > 0

    # Test with a state that cannot reach the goal
    impossible_state = State(
        [Predicate("at", Variable("n3")), Predicate("visited", Variable("n3"))]
    )

    # Reset planner state
    planner.visited_states = set()
    planner.solution = None

    # Since there's no way to visit n1 and n2 starting from n3 in our test domain,
    # this should fail to find a plan
    result = planner.dfs(impossible_state)
    assert result is False
    assert planner.solution is None


# Test complete planning process
def test_plan(setup_planner):
    planner = setup_planner

    # Get a plan
    plan = planner.plan()

    # Verify plan is not None and contains steps
    assert plan is not None
    assert len(plan) > 0

    # Verify the plan structure
    for step in plan:
        assert isinstance(step, tuple)
        assert len(step) == 2
        assert isinstance(step[0], str)  # Action name
        assert isinstance(step[1], dict)  # Bindings

    # Verify that the plan actually achieves the goal
    # by executing it step by step
    current_state = planner.initial_state
    for action_name, binding in plan:
        # Find the corresponding action
        action = None
        for a in planner.domain.actions:
            if a.name == action_name:
                action = a
                break

        assert action is not None

        # Apply the action
        current_state = planner.apply_action(current_state, action, binding)

    # Check that the final state satisfies the goal
    assert current_state.satisfies(planner.goal)


# Edge case: Test planning with already satisfied goal
def test_plan_already_satisfied():
    # Create a domain and problem where the goal is already satisfied in the initial state
    domain_str = """
    (define (domain simple-domain)
      (:requirements :strips)
      (:predicates (goal-state))
      (:action dummy
        :parameters ()
        :precondition (and)
        :effect (and (goal-state))
      )
    )
    """

    problem_str = """
    (define (problem simple-problem)
      (:domain simple-domain)
      (:init (goal-state))
      (:goal (goal-state))
    )
    """

    # Create temporary files
    fd1, domain_file = tempfile.mkstemp(suffix=".pddl")
    fd2, problem_file = tempfile.mkstemp(suffix=".pddl")

    with os.fdopen(fd1, "w") as f:
        f.write(domain_str)
    with os.fdopen(fd2, "w") as f:
        f.write(problem_str)

    try:
        domain = parse_domain(domain_file)
        problem = parse_problem(problem_file)

        planner = Planner(domain, problem)
        plan = planner.plan()

        # Plan should be empty list since goal is already satisfied
        assert plan is not None
        assert len(plan) == 0
    finally:
        # Cleanup
        os.remove(domain_file)
        os.remove(problem_file)


# Test with an unsolvable problem
def test_unsolvable_plan():
    # Create a domain and problem that is unsolvable
    domain_str = """
    (define (domain impossible-domain)
      (:requirements :strips)
      (:predicates (a) (b))
      (:action make-a
        :parameters ()
        :precondition (and)
        :effect (and (a))
      )
    )
    """

    problem_str = """
    (define (problem impossible-problem)
      (:domain impossible-domain)
      (:init (a))
      (:goal (b))
    )
    """

    # Create temporary files
    fd1, domain_file = tempfile.mkstemp(suffix=".pddl")
    fd2, problem_file = tempfile.mkstemp(suffix=".pddl")

    with os.fdopen(fd1, "w") as f:
        f.write(domain_str)
    with os.fdopen(fd2, "w") as f:
        f.write(problem_str)

    try:
        domain = parse_domain(domain_file)
        problem = parse_problem(problem_file)

        planner = Planner(domain, problem)
        plan = planner.plan()

        # No plan should be found
        assert plan is None
    finally:
        # Cleanup
        os.remove(domain_file)
        os.remove(problem_file)
