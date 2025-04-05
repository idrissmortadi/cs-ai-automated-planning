import argparse as ap
import logging

from pddl import parse_domain, parse_problem

from planner import Planner

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s -  %(levelname)s - %(message)s",
    filename="planner.log",
    filemode="w",
)
logger = logging.getLogger(__name__)


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
        plan_file = f"{problem.name}.pddl.plan"
        with open(plan_file, "w") as f:
            for i, step in enumerate(plan):
                logger.info(f"Step {i + 1}: {step}")
                print(step)
                f.write(f"( {step[0]} {' '.join(step[1].values())} )\n")
        logger.info(f"Plan written to {plan_file}")
    else:
        logger.warning("No plan found.")
        print("No plan found.")
