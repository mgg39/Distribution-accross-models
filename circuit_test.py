import numpy as np

from circuit import Circuit
from circuit_to_MB import circuit_to_graph, validate_graph
from circuit_to_qw import circuit_to_walk

# Example usage of the Circuit class
def main():
    circuit = Circuit(4)
    circuit.h(0)  # Hadamard on qubit 0
    circuit.cnot(0, 1)  # CNOT 0 -> 1
    circuit.cnot(0, 2)  # CNOT 0 -> 2
    circuit.cnot(0, 3)  # CNOT 0 -> 3
    circuit.rz(1, np.pi / 3)  # Rotate qubit 1 by RZ(pi/3)
    circuit.ry(2, np.pi / 4)  # Rotate qubit 2 by RY(pi/4)
    circuit.rx(3, np.pi / 6)  # Rotate qubit 3 by RX(pi/6)
    circuit.m(0, "X", None)  # Measure qubit 0 in X-basis
    circuit.m(1, "X-Y", np.pi / 3)  # Measure qubit 1 in X-Y plane
    circuit.m(2, "Y-Z", np.pi / 4)  # Measure qubit 2 in Y-Z plane
    circuit.m(3, "X-Z", np.pi / 6)  # Measure qubit 3 in X-Z plane

    print("Circuit: \n----------------------------")
    for instruction in circuit.instructions:
        print(instruction)
    
    print("Measurement based Graph state: \n----------------------------")
    graph_state = circuit_to_graph(circuit)
    print(graph_state)

    validate_graph(circuit, graph_state)

    print(" \n Quantum walk graph: \n----------------------------")
    walk_graph = circuit_to_walk(circuit)
    print(walk_graph)

if __name__ == "__main__":
    main()
