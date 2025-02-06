import numpy as np

from circuit import Circuit
from circuit_to_MB import circuit_to_graph, validate_graph
from circuit_to_qw import circuit_to_walk

# Example usage of the Circuit class
def main():
    circuit = Circuit(3)
    circuit.h(0)  # Hadamard on qubit 0
    circuit.cnot(0, 1)  # CX 0 -> 1
    circuit.ccx(0, 1, 2)  # CCX 0, 1 -> 2

    print("Circuit: \n----------------------------")
    for instruction in circuit.instructions:
        print(instruction)
    
    print("Measurement based Graph state: \n----------------------------")
    graph_state = circuit_to_graph(circuit)
    print(graph_state)

    validate_graph(circuit, graph_state)

if __name__ == "__main__":
    main()
