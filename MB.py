class GraphState:
    def __init__(self):
        self.nodes = []  # Nodes in the graph (qubits)
        self.edges = []  # Edges (entanglement)
        self.measurements = {}  # Use a dictionary for qubit-specific measurement instructions

    def add_node(self, qubit_id):
        self.nodes.append(qubit_id)

    def add_edge(self, qubit1, qubit2):
        self.edges.append((qubit1, qubit2))

    def add_measurement(self, qubit, basis, angle=None):
        self.measurements[qubit] = (basis, angle)

    def modify_basis_measurement(self, qubit, basis, angle=None):
        """Modify the measurement basis or angle for a qubit."""
        if qubit not in self.measurements:
            # Initialize a new entry for the qubit
            self.measurements[qubit] = (basis, angle)
        else:
            # Update an existing entry
            current_basis, current_angle = self.measurements[qubit]
            if current_basis != basis:
                raise ValueError(f"Conflicting basis changes for qubit {qubit}: {current_basis} vs {basis}")
            if angle is not None:
                new_angle = current_angle + angle if current_angle else angle
                self.measurements[qubit] = (basis, new_angle)

    def __str__(self):
        return f"Nodes: {self.nodes}\nEdges: {self.edges}\nMeasurements: {self.measurements}"


