import numpy as np

class Circuit:
    def __init__(self, width: int):
        self.width = width
        self.instructions = []
        self.active_qubits = set(range(width))

    def cnot(self, control: int, target: int):
        assert control in self.active_qubits
        assert target in self.active_qubits
        assert control != target
        self.instructions.append(("CNOT", control, target))

    def swap(self, qubit1: int, qubit2: int):
        assert qubit1 in self.active_qubits
        assert qubit2 in self.active_qubits
        assert qubit1 != qubit2
        self.instructions.append(("SWAP", qubit1, qubit2))

    def h(self, qubit: int):
        assert qubit in self.active_qubits
        self.instructions.append(("H", qubit))

    def s(self, qubit: int):
        assert qubit in self.active_qubits
        self.instructions.append(("S", qubit))

    def x(self, qubit: int):
        assert qubit in self.active_qubits
        self.instructions.append(("X", qubit))

    def y(self, qubit: int):
        assert qubit in self.active_qubits
        self.instructions.append(("Y", qubit))

    def z(self, qubit: int):
        assert qubit in self.active_qubits
        self.instructions.append(("Z", qubit))

    def rx(self, qubit: int, angle: float):
        assert qubit in self.active_qubits
        self.instructions.append(("RX", qubit, angle))

    def ry(self, qubit: int, angle: float):
        assert qubit in self.active_qubits
        self.instructions.append(("RY", qubit, angle))

    def rz(self, qubit: int, angle: float):
        assert qubit in self.active_qubits
        self.instructions.append(("RZ", qubit, angle))  # Append the angle directly

    def rzz(self, control: int, target: int, angle: float):
        assert control in self.active_qubits
        assert target in self.active_qubits
        self.instructions.append(("RZZ", control, target, angle))  # Append angle directly

    def ccx(self, control1: int, control2: int, target: int):
        assert control1 in self.active_qubits
        assert control2 in self.active_qubits
        assert target in self.active_qubits
        assert control1 != control2 and control1 != target and control2 != target

        self.instructions.append(("CCX", control1, control2, target))  # Simplified CCX representation

    def i(self, qubit: int):
        assert qubit in self.active_qubits
        self.instructions.append(("I", qubit))

    def m(self, qubit: int, plane: str, angle: float):
        assert qubit in self.active_qubits
        self.instructions.append(("M", qubit, plane, angle))
        self.active_qubits.remove(qubit)
