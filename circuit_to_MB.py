import numpy as np

from circuit import Circuit
from MB import GraphState

# conversion function
def circuit_to_graph(circuit):
    graph = GraphState()
    
    # Create graph nodes for each qubit
    for i in range(circuit.width):
        graph.add_node(i)

    # Parse circuit instructions
def circuit_to_graph(circuit):
    graph = GraphState()

    # Create graph nodes for each qubit
    for i in range(circuit.width):
        graph.add_node(i)

    # Parse circuit instructions
    for instruction in circuit.instructions:
        if instruction[0] == "H":
            pass  # H modifies state, no explicit measurement
        elif instruction[0] == "CNOT":
            control, target = instruction[1], instruction[2]
            graph.add_edge(control, target)  # Add entanglement edge
        elif instruction[0] == "SWAP":
            qubit1, qubit2 = instruction[1], instruction[2]
            graph.add_edge(qubit1, qubit2)  # Represent interaction
        elif instruction[0] == "RZ":
            qubit, angle = instruction[1], instruction[2]
            graph.modify_basis_measurement(qubit, "X-Y", angle)  # Modify basis
        elif instruction[0] == "RY":
            qubit, angle = instruction[1], instruction[2]
            graph.modify_basis_measurement(qubit, "Y-Z", angle)  # Modify basis
        elif instruction[0] == "RX":
            qubit, angle = instruction[1], instruction[2]
            graph.modify_basis_measurement(qubit, "X-Z", angle)  # Modify basis
        elif instruction[0] == "Z":
            qubit = instruction[1]
            graph.modify_basis_measurement(qubit, "Z", None)  # Modify basis
        elif instruction[0] == "Y":
            qubit = instruction[1]
            graph.modify_basis_measurement(qubit, "Y", None)  # Modify basis
        elif instruction[0] == "S":
            qubit = instruction[1]
            graph.modify_basis_measurement(qubit, "X-Y", np.pi / 2)  # S acts as RZ(pi/2)
        elif instruction[0] == "M":
            qubit, plane, angle = instruction[1], instruction[2], instruction[3]
            graph.add_measurement(qubit, plane, angle)  # Add explicit measurement
        elif instruction[0] == "RZZ":
            control, target, angle = instruction[1], instruction[2], instruction[3]
            graph.add_edge(control, target)  # Add entanglement edge
        elif instruction[0] == "CCX":
            control1, control2, target = instruction[1], instruction[2], instruction[3]
            graph.add_edge(control1, control2)
            graph.add_edge(control1, target)
            graph.add_edge(control2, target)
        else:
            raise ValueError(f"Unknown instruction '{instruction[0]}' encountered.")

    return graph

def validate_graph(circuit, graph):
    errors = []

    # 1. Check nodes
    if len(graph.nodes) != circuit.width:
        errors.append(f"Node count mismatch: Expected {circuit.width}, found {len(graph.nodes)}")

    # 2. Check edges
    expected_edges = []
    for instruction in circuit.instructions:
        if instruction[0] == "CNOT":
            control, target = instruction[1], instruction[2]
            expected_edges.append((control, target))
        elif instruction[0] == "SWAP":
            qubit1, qubit2 = instruction[1], instruction[2]
            expected_edges.append((qubit1, qubit2))

    for edge in expected_edges:
        if edge not in graph.edges:
            errors.append(f"Missing edge: {edge}")
    for edge in graph.edges:
        if edge not in expected_edges:
            errors.append(f"Unexpected edge: {edge}")

    # 3. Check measurements
    measured_qubits = set()
    for instruction in circuit.instructions:
        if instruction[0] == "M":
            qubit, plane, angle = instruction[1], instruction[2], instruction[3]
            if qubit in measured_qubits:
                errors.append(f"Duplicate measurement for qubit {qubit}")
            measured_qubits.add(qubit)
            if qubit not in graph.measurements:
                errors.append(f"Missing measurement for qubit {qubit}")
            else:
                basis, graph_angle = graph.measurements[qubit]
                if basis != plane:
                    errors.append(f"Basis mismatch for qubit {qubit}: Expected {plane}, found {basis}")
                if graph_angle != angle:
                    errors.append(f"Angle mismatch for qubit {qubit}: Expected {angle}, found {graph_angle}")

    # 4. Logical consistency of rotations
    for instruction in circuit.instructions:
        if instruction[0] in {"RZ", "RY", "RX"}:
            qubit, angle = instruction[1], instruction[2]
            if qubit in measured_qubits:
                basis, graph_angle = graph.measurements[qubit]
                expected_basis = {"RZ": "X-Y", "RY": "Y-Z", "RX": "X-Z"}[instruction[0]]
                if basis != expected_basis:
                    errors.append(f"Basis mismatch after rotation for qubit {qubit}: Expected {expected_basis}, found {basis}")
                if abs(graph_angle - angle) > 1e-6:
                    errors.append(f"Angle mismatch after rotation for qubit {qubit}: Expected {angle}, found {graph_angle}")

    # Return validation result
    if not errors:
        print("Graph validation passed!")
    else:
        print("Graph validation failed with errors:")
        for error in errors:
            print(f"- {error}")

