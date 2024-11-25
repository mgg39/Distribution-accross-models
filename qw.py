import numpy as np

class QuantumWalkGraph:
    def __init__(self):
        self.nodes = []  # Nodes (qubits)
        self.edges = []  # Edges (entanglement or connectivity)
        self.walker_state = {}  # Walker state on nodes

    def add_node(self, qubit_id):
        if qubit_id not in self.nodes:
            self.nodes.append(qubit_id)
            self.walker_state[qubit_id] = None  # Initialize walker state

    def add_edge(self, qubit1, qubit2):
        if (qubit1, qubit2) not in self.edges and (qubit2, qubit1) not in self.edges:
            self.edges.append((qubit1, qubit2))

    def set_walker_state(self, qubit, state):
        self.walker_state[qubit] = state

    def __str__(self):
        return f"Nodes: {self.nodes}\nEdges: {self.edges}\nWalker State: {self.walker_state}"

