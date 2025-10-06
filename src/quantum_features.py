import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

def ry_feature_map_angles(amp_vec: np.ndarray, n_qubits: int):
    x = amp_vec[:n_qubits]
    return np.tanh(x) * np.pi

def build_feature_map(n_qubits: int, depth: int):
    def simulate(angles: np.ndarray):
        qc = QuantumCircuit(n_qubits)
        for _ in range(depth):
            for q in range(n_qubits):
                qc.ry(float(angles[q]), q)
            for q in range(n_qubits - 1):
                qc.cz(q, q + 1)
        return Statevector.from_instruction(qc)
    return simulate

def z_expectations_from_statevector(sv: Statevector, n_qubits: int):
    probs = np.abs(sv.data) ** 2
    z_expects = np.zeros(n_qubits, dtype=np.float32)
    for q in range(n_qubits):
        mask = 1 << (n_qubits - 1 - q)
        p0 = probs[[i for i in range(len(probs)) if (i & mask) == 0]].sum()
        p1 = probs[[i for i in range(len(probs)) if (i & mask) != 0]].sum()
        z_expects[q] = float(p0 - p1)
    return z_expects