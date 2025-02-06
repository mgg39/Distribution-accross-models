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
            # Allow X → X-Z conversion but prevent incompatible transitions
            if current_basis == "X" and basis == "X-Z":
                pass  # Allow this
            elif current_basis != basis:
                raise ValueError(f"Conflicting basis changes for qubit {qubit}: {current_basis} vs {basis}")
            if angle is not None:
                self.measurements[qubit] = (basis, (current_angle or 0) + angle) 

    def add_hadamard(self, qubit):
        """
        In MBQC, applying a Hadamard gate means changing the measurement basis.
        - If measuring in Z-basis → Measure in X-basis.
        - If measuring in X-basis → Measure in Z-basis.
        - If Hadamard at start → Just treat qubit as pre-prepared in |+> instead of |0>.
        """
        if qubit in self.measurements:
            basis, angle = self.measurements[qubit]
            if basis == "Z":
                new_basis = "X"
            elif basis == "X":
                new_basis = "Z"
            else:
                new_basis = basis  # Leave unchanged for non-Z/X bases
            self.measurements[qubit] = (new_basis, angle)
        else:
            # If no measurement, assume initial preparation in |+>
            self.measurements[qubit] = ("X", None)

    def __str__(self):
        return f"Nodes: {self.nodes}\nEdges: {self.edges}\nMeasurements: {self.measurements}"


