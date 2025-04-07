echo "Benchmark Report" > benchmarks.log
echo "================" >> benchmarks.log

alias lpg-td='./LPG-td-1.4/lpg-td'

echo "Running Fast Downward (Small Problem)"
echo "Planner: Fast Downward (Small Problem)" >> benchmarks.log
{ time fast-downward-24.06.1/fast-downward.py --alias lama-first hamiltonian_cycle/domain.pddl hamiltonian_cycle/problem-small.pddl; } 2>> benchmarks.log
echo "----------------" >> benchmarks.log

echo "Running Fast Downward (Medium Problem)"
echo "Planner: Fast Downward (Medium Problem)" >> benchmarks.log
{ time fast-downward-24.06.1/fast-downward.py --alias lama-first hamiltonian_cycle/domain.pddl hamiltonian_cycle/problem-medium.pddl; } 2>> benchmarks.log
echo "----------------" >> benchmarks.log

echo "Running Fast Downward (Large Problem)"
echo "Planner: Fast Downward (Large Problem)" >> benchmarks.log
{ time fast-downward-24.06.1/fast-downward.py --alias lama-first hamiltonian_cycle/domain.pddl hamiltonian_cycle/problem-large.pddl; } 2>> benchmarks.log
echo "----------------" >> benchmarks.log

echo "Running FF Planner (Small Problem)"
echo "Planner: FF Planner (Small Problem)" >> benchmarks.log
{ time ff hamiltonian_cycle/domain.pddl hamiltonian_cycle/problem-small.pddl; } 2>> benchmarks.log
echo "----------------" >> benchmarks.log

echo "Running FF Planner (Medium Problem)"
echo "Planner: FF Planner (Medium Problem)" >> benchmarks.log
{ time ff hamiltonian_cycle/domain.pddl hamiltonian_cycle/problem-medium.pddl; } 2>> benchmarks.log
echo "----------------" >> benchmarks.log

echo "Running FF Planner (Large Problem)"
echo "Planner: FF Planner (Large Problem)" >> benchmarks.log
{ time ff hamiltonian_cycle/domain.pddl hamiltonian_cycle/problem-large.pddl; } 2>> benchmarks.log
echo "----------------" >> benchmarks.log

echo "Running LPG-td (Small Problem)"
echo "Planner LPG-td (Small Problem)" >> benchmarks.log
{ time lpg-td -o hamiltonian_cycle/domain.pddl -f hamiltonian_cycle/problem-small.pddl -n 1; } 2>> benchmarks.log
echo "----------------" >> benchmarks.log

echo "Running LPG-td (Medium Problem)"
echo "Planner LPG-td (Medium Problem)" >> benchmarks.log
{ time lpg-td -o hamiltonian_cycle/domain.pddl -f hamiltonian_cycle/problem-medium.pddl -n 1; } 2>> benchmarks.log
echo "----------------" >> benchmarks.log

echo "Running LPG-td (Large Problem)"
echo "Planner LPG-td (Large Problem)" >> benchmarks.log
{ time lpg-td -o hamiltonian_cycle/domain.pddl -f hamiltonian_cycle/problem-large.pddl -n 1; } 2>> benchmarks.log
echo "----------------" >> benchmarks.log

echo "Running DFS Planner (Small Problem)"
echo "Planner: DFS Planner (Small Problem)" >> benchmarks.log
{ time python planner/dfs_planner.py -d hamiltonian_cycle/domain.pddl -p hamiltonian_cycle/problem-small.pddl; } 2>> benchmarks.log
echo "----------------" >> benchmarks.log

echo "Running DFS Planner (Medium Problem)"
echo "Planner: DFS Planner (Medium Problem)" >> benchmarks.log
{ time python planner/dfs_planner.py -d hamiltonian_cycle/domain.pddl -p hamiltonian_cycle/problem-medium.pddl; } 2>> benchmarks.log
echo "----------------" >> benchmarks.log

# echo "Running DFS Planner (Large Problem)"
# echo "Planner: DFS Planner (Large Problem)" >> benchmarks.log
# { time python planner/dfs_planner.py -d hamiltonian_cycle/domain.pddl -p hamiltonian_cycle/problem-large.pddl; } 2>> benchmarks.log
# echo "----------------" >> benchmarks.log