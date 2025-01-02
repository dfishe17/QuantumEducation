import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator, QasmSimulator
from qiskit.quantum_info import Statevector
from qiskit.visualization import circuit_drawer
from qiskit.exceptions import QiskitError
import time

class QuantumComputer:
    def __init__(self):
        self.simulator = AerSimulator(method='statevector')
        self.qasm_sim = QasmSimulator()
        self.gates = ['H', 'X', 'Y', 'Z', 'CNOT', 'CZ']
        self.gate_descriptions = {
            'H': 'Hadamard Gate - Creates superposition',
            'X': 'Pauli-X Gate - Bit flip',
            'Y': 'Pauli-Y Gate - Combined bit and phase flip',
            'Z': 'Pauli-Z Gate - Phase flip',
            'CNOT': 'Controlled-NOT Gate - Two-qubit controlled bit flip',
            'CZ': 'Controlled-Z Gate - Two-qubit controlled phase flip'
        }
        self.performance_data = {}

    def get_available_gates(self):
        """Return list of available quantum gates."""
        return self.gates

    def simulate_circuit(self, circuit_operations):
        """Simulate a quantum circuit using Qiskit with performance tracking."""
        try:
            self.performance_data = {}  # Reset performance data

            # Calculate number of qubits needed
            num_qubits = 1
            for op in circuit_operations:
                num_qubits = max(num_qubits, op.get('target', 0) + 1)
                if 'control' in op:
                    num_qubits = max(num_qubits, op['control'] + 1)

            # Create quantum circuit
            qc = QuantumCircuit(num_qubits)

            # Add gates to circuit with performance tracking
            for i, op in enumerate(circuit_operations):
                start_time = time.time()
                gate = op['gate']
                target = op.get('target', 0)

                # Apply gate and measure performance
                try:
                    if gate == 'H':
                        qc.h(target)
                    elif gate == 'X':
                        qc.x(target)
                    elif gate == 'Y':
                        qc.y(target)
                    elif gate == 'Z':
                        qc.z(target)
                    elif gate == 'CNOT' and 'control' in op:
                        qc.cx(op['control'], target)
                    elif gate == 'CZ' and 'control' in op:
                        qc.cz(op['control'], target)

                    # Calculate gate fidelity (simplified model)
                    fidelity = 1.0
                    if gate in ['CNOT', 'CZ']:  # Two-qubit gates have lower fidelity
                        fidelity = 0.95
                    elif gate in ['X', 'Y', 'Z']:  # Single-qubit gates have high fidelity
                        fidelity = 0.99
                    else:
                        fidelity = 0.97

                    # Add noise effect based on circuit depth
                    depth_factor = 1.0 - (0.01 * i)  # Decrease fidelity with circuit depth
                    fidelity *= max(0.8, depth_factor)

                    # Record performance metrics
                    self.performance_data[f"step_{i}"] = {
                        'gate': gate,
                        'time': (time.time() - start_time) * 1000,  # Convert to ms
                        'fidelity': fidelity,
                        'target': target,
                        'control': op.get('control', None)
                    }

                except Exception as e:
                    self.performance_data[f"step_{i}"] = {
                        'gate': gate,
                        'error': str(e),
                        'fidelity': 0.0
                    }
                    raise e

            # Create statevector circuit and run simulation
            sv_qc = qc.copy()
            qc_transpiled = transpile(sv_qc, self.simulator)
            job = self.simulator.run(qc_transpiled)
            result = job.result()

            # Get statevector
            statevector = Statevector.from_instruction(qc)
            if not isinstance(statevector, np.ndarray):
                statevector = statevector.data

            # Normalize
            norm = np.sqrt(np.sum(np.abs(statevector) ** 2))
            if not np.isclose(norm, 1.0, atol=1e-7):
                statevector = statevector / norm

            # Update measurement section
            qc.measure_all()
            meas_result = self.qasm_sim.run(qc, shots=1000).result()
            counts = meas_result.get_counts()

            # Format measurements
            measurements = {
                state: {
                    'count': count,
                    'probability': count / 1000,
                    'basis_state': f"|{state}⟩"
                }
                for state, count in counts.items()
            }

            return {
                'state_vector': statevector,
                'measurements': measurements,
                'performance_data': self.performance_data,
                'success': True
            }

        except Exception as e:
            return {
                'error': f"Simulation error: {str(e)}",
                'success': False
            }

    def validate_circuit(self, circuit_operations):
        """Validate circuit operations before simulation."""
        if not circuit_operations:
            raise ValueError("Circuit is empty. Please add quantum gates.")

        for i, op in enumerate(circuit_operations):
            if 'gate' not in op:
                raise ValueError(f"Operation #{i+1} is missing gate type.")
            if op['gate'] not in self.gates:
                raise ValueError(f"Operation #{i+1} uses invalid gate '{op['gate']}'")
            if 'target' not in op:
                raise ValueError(f"Operation #{i+1} is missing target qubit.")
            if op['gate'] in ['CNOT', 'CZ'] and 'control' not in op:
                raise ValueError(f"Operation #{i+1} requires control qubit.")

def run_sample_circuit():
    """Run a sample quantum circuit (Hadamard gate on |0⟩ state)."""
    qc = QuantumComputer()
    circuit_ops = [{'gate': 'H', 'target': 0}]
    return qc.simulate_circuit(circuit_ops)

def calculate_bloch_coordinates(state_vector):
    """Calculate Bloch sphere coordinates from state vector."""
    x = 2 * np.real(np.conj(state_vector[0]) * state_vector[1])
    y = 2 * np.imag(np.conj(state_vector[0]) * state_vector[1])
    z = np.abs(state_vector[0])**2 - np.abs(state_vector[1])**2
    return x, y, z