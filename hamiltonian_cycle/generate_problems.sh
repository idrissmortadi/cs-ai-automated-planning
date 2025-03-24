EDGE_PROBS=(0.3 0.6 0.9)
VERTEX_COUNTS=(5 12 30)

for edge_prob in "${EDGE_PROBS[@]}"; do
    for vertex_count in "${VERTEX_COUNTS[@]}"; do
        edge_prob_int=$(echo "$edge_prob * 100" | bc | awk '{print int($1+0.5)}')
        problem_file="problem_v${vertex_count}_p${edge_prob_int}.pddl"
        python hamiltonian_cycle.py --vertices "$vertex_count" --edge-prob "$edge_prob" --problem "$problem_file"
    done
done