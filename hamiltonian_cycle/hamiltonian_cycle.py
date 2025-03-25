import argparse
import random
import re
import subprocess

import matplotlib.pyplot as plt
import networkx as nx


def generate_random_graph(num_vertices, edge_probability=0.5):
    """Generate a random connected graph with the given number of vertices."""
    graph = nx.Graph()

    # Add vertices
    for i in range(1, num_vertices + 1):
        graph.add_node(i)

    # Add random edges
    for i in range(1, num_vertices + 1):
        for j in range(i + 1, num_vertices + 1):
            if random.random() < edge_probability:
                graph.add_edge(i, j)

    # Ensure the graph is connected
    while not nx.is_connected(graph):
        components = list(nx.connected_components(graph))
        if len(components) > 1:
            comp1 = random.choice(list(components[0]))
            comp2 = random.choice(list(components[1]))
            graph.add_edge(comp1, comp2)

    return graph


def generate_pddl_edges(graph):
    """Generate PDDL representation of the graph edges."""
    pddl_edges = []
    for u, v in graph.edges():
        pddl_edges.append(f"    (connected v{u} v{v})")
        pddl_edges.append(f"    (connected v{v} v{u})")
    return "\n".join(pddl_edges)


def create_problem_file(output_path, graph, num_vertices):
    """Create a problem file for a graph with the given number of vertices."""
    # Generate vertex objects
    vertex_objects = (
        " ".join([f"v{i}" for i in range(1, num_vertices + 1)]) + " - vertex"
    )

    # Generate count objects (need n0 through nN where N = num_vertices)
    count_objects = " ".join([f"n{i}" for i in range(num_vertices + 1)]) + " - count"

    # Generate edges
    graph_edges = generate_pddl_edges(graph)

    # Generate count sequence
    count_sequence = "\n".join(
        [f"    (next n{i} n{i + 1})" for i in range(num_vertices)]
    )

    # Generate visited goals
    visited_goals = "\n      ".join(
        [f"(visited v{i})" for i in range(1, num_vertices + 1)]
    )

    # Total vertices
    total_vertices = f"n{num_vertices}"

    # Create the content with substitutions
    with open("problem-template.pddl", "r") as file:
        content = file.read()
        content = content.replace("{VERTEX_OBJECTS}", vertex_objects)
        content = content.replace("{COUNT_OBJECTS}", count_objects)
        content = content.replace("{GRAPH_EDGES}", graph_edges)
        content = content.replace("{COUNT_SEQUENCE}", count_sequence)
        content = content.replace("{VISITED_GOALS}", visited_goals)
        content = content.replace("{TOTAL_VERTICES}", total_vertices)

    with open(output_path, "w") as file:
        file.write(content)


def run_planner(domain_file, problem_file):
    """Run the FF planner and return the output."""
    try:
        result = subprocess.run(
            ["ff", domain_file, problem_file],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Planner error: {e}")
        print(f"Error output: {e.stderr}")
        return e.stdout if e.stdout else ""


def parse_plan(planner_output):
    """Parse the planner output to extract the plan steps."""
    plan = []
    in_plan_section = False

    for line in planner_output.split("\n"):
        if "found legal plan as follows" in line:
            in_plan_section = True
            continue

        if in_plan_section:
            # Match lines like "step    0: SELECT-START V5 N0 N1"
            # or lines like "        1: MOVE-TO-NEXT V5 V4 N1 N2"
            action_match = re.search(r"\d+:\s+(\w+(?:-\w+)*)\s+(.*)", line)
            if action_match:
                action_name = action_match.group(1)
                action_params = action_match.group(2).strip().split()

                # Skip REACH-GOAL as it's not part of the actual plan
                if action_name != "REACH-GOAL":
                    plan.append((action_name, action_params))

            elif "time spent:" in line:
                break

    return plan


def extract_cycle_from_plan(plan):
    """Extract the vertices in cycle order from the plan."""
    cycle = []
    current_vertex = None

    for action_name, params in plan:
        if action_name == "SELECT-START":
            vertex = params[0].lstrip("V")
            cycle.append(int(vertex))
            current_vertex = int(vertex)

        elif action_name == "MOVE-TO-NEXT":
            from_vertex = params[0].lstrip("V")
            to_vertex = params[1].lstrip("V")
            assert int(from_vertex) == current_vertex
            cycle.append(int(to_vertex))
            current_vertex = int(to_vertex)

        elif action_name == "COMPLETE-CYCLE":
            # Just verify we're back at the start
            from_vertex = params[0].lstrip("V")
            to_vertex = params[1].lstrip("V")
            assert int(from_vertex) == current_vertex
            assert int(to_vertex) == cycle[0]

    return cycle


def plot_graph_and_solution(graph, cycle=None, output_path="graph_solution.png"):
    """Plot the graph and the Hamiltonian cycle solution."""
    plt.figure(figsize=(12, 10))

    # Position nodes using spring layout with fixed seed for reproducibility
    pos = nx.spring_layout(graph, seed=42)

    # Draw all edges in light gray
    nx.draw_networkx_edges(graph, pos, width=1.0, alpha=0.3, edge_color="gray")

    # Draw cycle edges if a cycle was found
    if cycle:
        cycle_edges = [(cycle[i], cycle[i + 1]) for i in range(len(cycle) - 1)]
        cycle_edges.append((cycle[-1], cycle[0]))  # Close the cycle
        nx.draw_networkx_edges(
            graph, pos, edgelist=cycle_edges, width=3.0, alpha=1.0, edge_color="red"
        )

        # Add path sequence numbers to edges
        edge_labels = {}
        for i in range(len(cycle) - 1):
            edge_labels[(cycle[i], cycle[i + 1])] = f"{i + 1}"
        # The last edge connects back to the start
        edge_labels[(cycle[-1], cycle[0])] = f"{len(cycle)}"
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=10)

        title = "Hamiltonian Cycle Solution"
    else:
        title = "Graph Structure"

    # Draw nodes
    nx.draw_networkx_nodes(graph, pos, node_size=700, node_color="lightblue")

    # Draw labels
    labels = {i: f"v{i}" for i in graph.nodes()}
    nx.draw_networkx_labels(graph, pos, labels, font_size=14, font_weight="bold")

    plt.axis("off")
    plt.title(title, fontsize=16)
    plt.tight_layout()

    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Graph visualization saved to {output_path}")


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Solve Hamiltonian Cycle problems with PDDL planning."
    )

    parser.add_argument(
        "--vertices",
        "-v",
        type=int,
        default=8,
        help="Number of vertices in the graph (default: 8)",
    )

    parser.add_argument(
        "--edge-prob",
        "-p",
        type=float,
        default=0.5,
        help="Probability of edge creation between vertices (default: 0.5)",
    )

    parser.add_argument(
        "--domain",
        "-d",
        type=str,
        default="domain.pddl",
        help="Path to the domain PDDL file (default: domain.pddl)",
    )

    parser.add_argument(
        "--problem",
        "-o",
        type=str,
        default="problem.pddl",
        help="Path to output the problem PDDL file (default: problem.pddl)",
    )

    parser.add_argument(
        "--original-graph",
        type=str,
        default=None,
        help="Filename for the original graph visualization (default: based on problem filename)",
    )

    parser.add_argument(
        "--solution-graph",
        type=str,
        default=None,
        help="Filename for the solution graph visualization (default: based on problem filename)",
    )

    return parser.parse_args()


def main():
    # Parse arguments
    args = parse_arguments()

    # Parameters from command line
    num_vertices = args.vertices
    edge_probability = args.edge_prob
    domain_path = args.domain
    problem_path = args.problem

    # Generate plot filenames based on problem filename if not specified
    problem_base = (
        problem_path.rsplit(".", 1)[0] if "." in problem_path else problem_path
    )
    original_graph_path = args.original_graph or f"{problem_base}_original.png"
    solution_graph_path = args.solution_graph or f"{problem_base}_solution.png"

    # Generate graph
    graph = generate_random_graph(num_vertices, edge_probability)

    # Create problem file
    create_problem_file(problem_path, graph, num_vertices)

    # Create visualization of initial graph
    plot_graph_and_solution(graph, cycle=None, output_path=original_graph_path)

    print(
        f"Generated graph with {num_vertices} vertices and {len(graph.edges())} edges"
    )
    print(f"PDDL problem file saved to {problem_path}")

    # Run planner
    print("Running FF planner...")
    planner_output = run_planner(domain_path, problem_path)

    # Save planner output to file
    with open("planner_output.txt", "w") as f:
        f.write(planner_output)
    print("Planner output saved to planner_output.txt")

    # Parse plan
    plan = parse_plan(planner_output)
    if plan:
        print("\nExtracted plan:")
        for i, (action, params) in enumerate(plan):
            print(f"{i}: {action} {' '.join(params)}")

        # Extract and visualize cycle
        cycle = extract_cycle_from_plan(plan)
        print(
            f"\nHamiltonian cycle: {' → '.join([f'v{v}' for v in cycle])} → v{cycle[0]}"
        )
        plot_graph_and_solution(graph, cycle, output_path=solution_graph_path)
    else:
        print("\nNo plan found in the planner output.")


if __name__ == "__main__":
    main()
