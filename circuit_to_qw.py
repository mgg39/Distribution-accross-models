import numpy as np
from qw import QuantumWalkGraph
from circuit import Circuit

def circuit_to_walk(circuit):
    graph = QuantumWalkGraph()

    # Create graph nodes for each qubit
    for i in range(circuit.width):
        graph.add_node(i)

    # Parse circuit instructions
    for instruction in circuit.instructions:
        if instruction[0] == "H":
            qubit = instruction[1]
            graph.set_walker_state(qubit, "superposition")  # H creates superposition
        elif instruction[0] == "CNOT":
            control, target = instruction[1], instruction[2]
            graph.add_edge(control, target)  # Add entanglement as an edge
        elif instruction[0] == "SWAP":
            qubit1, qubit2 = instruction[1], instruction[2]
            graph.add_edge(qubit1, qubit2)  # Represent interaction
        elif instruction[0] == "X":
            qubit = instruction[1]
            graph.set_walker_state(qubit, "flip")  # X flips the walker’s state
        elif instruction[0] == "Z":
            qubit = instruction[1]
            graph.set_walker_state(qubit, "phase_flip")  # Z applies a phase flip
        elif instruction[0] in {"RZ", "RY", "RX"}:
            qubit, angle = instruction[1], instruction[2]
            rotation_type = {"RZ": "Z-rotation", "RY": "Y-rotation", "RX": "X-rotation"}[instruction[0]]
            graph.set_walker_state(qubit, f"{rotation_type}({angle:.2f})")  # Record rotation
        elif instruction[0] == "M":
            qubit, plane, angle = instruction[1], instruction[2], instruction[3]
            if angle is not None:
                graph.set_walker_state(qubit, f"measure({plane}, {angle:.2f})")  # Format angle if it exists
            else:
                graph.set_walker_state(qubit, f"measure({plane}, None)")  # Handle None angle
        elif instruction[0] == "RZZ":
            control, target, angle = instruction[1], instruction[2], instruction[3]
            graph.add_edge(control, target)  # Entanglement edge
            graph.set_walker_state(control, f"RZZ({angle:.2f})")
        else:
            raise ValueError(f"Unknown instruction '{instruction[0]}' encountered.")

    return graph