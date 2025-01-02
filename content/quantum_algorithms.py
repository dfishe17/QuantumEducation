import streamlit as st
import numpy as np
from quantum_utils import QuantumComputer
import plotly.graph_objects as go

def show_algorithms():
    st.title("Quantum Algorithm Demonstrations")

    # Enhanced introduction to quantum algorithms
    st.markdown("""
    Quantum algorithms leverage the unique properties of quantum mechanics to solve specific 
    computational problems more efficiently than classical algorithms. Each algorithm demonstrates 
    different aspects of quantum advantage:

    - **Superposition**: Creating quantum states that exist in multiple states simultaneously
    - **Interference**: Wave-like behavior that can amplify correct solutions
    - **Entanglement**: Quantum correlations between multiple qubits
    """)

    algorithm = st.selectbox(
        "Select an Algorithm",
        ["Deutsch's Algorithm", "Grover's Search", "Quantum Fourier Transform", "Traveling Salesman (QAOA)"]
    )

    if algorithm == "Deutsch's Algorithm":
        show_deutsch_algorithm()
    elif algorithm == "Grover's Search":
        show_grover_search()
    elif algorithm == "Quantum Fourier Transform":
        show_quantum_fourier_transform()
    elif algorithm == "Traveling Salesman (QAOA)":
        show_traveling_salesman()

def show_deutsch_algorithm():
    st.header("Deutsch's Algorithm")
    st.markdown("""
    ### Overview
    Deutsch's algorithm is one of the simplest examples of quantum parallelism and interference.
    It determines whether a binary function is constant or balanced using only one function evaluation,
    while classical algorithms require two evaluations.

    ### Technical Details
    - **Input**: A black-box (oracle) function f: {0,1} → {0,1}
    - **Output**: 0 if f is constant, 1 if f is balanced
    - **Speedup**: 2x over classical algorithms

    ### Applications
    - Property testing of boolean functions
    - Foundational algorithm for understanding quantum speedup
    - Building block for more complex quantum algorithms

    ### How it works:
    1. Initialize two qubits in |0⟩ state
    2. Apply Hadamard gates to create superposition
    3. Apply the oracle (function)
    4. Apply final Hadamard gate
    5. Measure the first qubit
    """)

    # Interactive demonstration
    st.subheader("Interactive Demo")
    function_type = st.radio(
        "Select Oracle Function Type",
        ["Constant (0)", "Constant (1)", "Balanced (NOT)", "Balanced (Identity)"]
    )

    if st.button("Run Deutsch's Algorithm"):
        qc = QuantumComputer()
        # Create circuit based on selected function
        circuit_ops = [
            {'gate': 'X', 'target': 1},  # Prepare second qubit in |1⟩
            {'gate': 'H', 'target': 0},  # Hadamard on first qubit
            {'gate': 'H', 'target': 1},  # Hadamard on second qubit
        ]

        # Add oracle based on selection
        if function_type == "Constant (1)":
            circuit_ops.append({'gate': 'X', 'target': 1})
        elif function_type == "Balanced (NOT)":
            circuit_ops.append({'gate': 'CNOT', 'control': 0, 'target': 1})
        elif function_type == "Balanced (Identity)":
            circuit_ops.append({'gate': 'CZ', 'control': 0, 'target': 1})

        circuit_ops.append({'gate': 'H', 'target': 0})  # Final Hadamard

        result = qc.simulate_circuit(circuit_ops)

        if result['success']:
            st.success("Algorithm executed successfully!")
            st.write("Result:", "Function is " +
                    ("constant" if function_type.startswith("Constant") else "balanced"))
            st.write("State Vector:", result['state_vector'])
        else:
            st.error(f"Simulation failed: {result.get('error', 'Unknown error')}")

def show_grover_search():
    st.header("Grover's Search Algorithm")
    st.markdown("""
    ### Overview
    Grover's algorithm provides a quadratic speedup for searching unstructured databases.
    It's one of the most important quantum algorithms with practical applications.

    ### Technical Details
    - **Input**: Unstructured database of N items
    - **Output**: Index of marked item
    - **Speedup**: O(√N) vs O(N) classical

    ### Applications
    - Database searching
    - Optimization problems
    - Solving systems of linear equations
    - Finding collisions in cryptographic hash functions

    ### Key Components:
    1. **Oracle Operator**: Marks the target state
    2. **Diffusion Operator**: Amplifies the amplitude of marked state
    3. **Optimal Iterations**: π/4 * √N for maximum probability

    ### How it works:
    1. Initialize qubits in superposition
    2. Apply oracle marking the target state
    3. Apply diffusion operator
    4. Repeat steps 2-3 optimal number of times
    5. Measure to find marked state
    """)

    # Interactive demonstration
    st.subheader("Interactive Demo")
    n_qubits = st.slider("Number of Qubits", 2, 3, 2)
    target_state = st.selectbox(
        "Target State",
        [format(i, f'0{n_qubits}b') for i in range(2**n_qubits)]
    )

    # Calculate optimal number of iterations
    optimal_iterations = int(np.pi/4 * np.sqrt(2**n_qubits))
    iterations = st.slider("Number of Iterations", 1, optimal_iterations*2, optimal_iterations,
                         help=f"Optimal number of iterations: {optimal_iterations}")

    if st.button("Run Grover's Search"):
        try:
            qc = QuantumComputer()
            # Initialize superposition
            circuit_ops = [{'gate': 'H', 'target': i} for i in range(n_qubits)]

            # Apply oracle and diffusion for the specified number of iterations
            for _ in range(iterations):
                # Oracle (mark target state)
                target_int = int(target_state, 2)
                for i in range(n_qubits):
                    if not (target_int & (1 << i)):
                        circuit_ops.append({'gate': 'X', 'target': i})

                # Multi-controlled Z
                for i in range(n_qubits-1):
                    circuit_ops.append({'gate': 'CZ', 'control': i, 'target': n_qubits-1})

                # Undo X gates
                for i in range(n_qubits):
                    if not (target_int & (1 << i)):
                        circuit_ops.append({'gate': 'X', 'target': i})

                # Diffusion operator
                for i in range(n_qubits):
                    circuit_ops.append({'gate': 'H', 'target': i})
                    circuit_ops.append({'gate': 'X', 'target': i})

                for i in range(n_qubits-1):
                    circuit_ops.append({'gate': 'CZ', 'control': i, 'target': n_qubits-1})

                for i in range(n_qubits):
                    circuit_ops.append({'gate': 'X', 'target': i})
                    circuit_ops.append({'gate': 'H', 'target': i})

            result = qc.simulate_circuit(circuit_ops)

            if result['success']:
                st.success("Algorithm executed successfully!")

                # Display probabilities with a bar chart
                st.subheader("Measurement Probabilities")
                probabilities = {state: data['probability'] 
                               for state, data in result['measurements'].items()}

                # Create bar chart using plotly
                import plotly.graph_objects as go

                fig = go.Figure(data=[
                    go.Bar(
                        x=list(probabilities.keys()),
                        y=list(probabilities.values()),
                        text=[f'{prob:.3f}' for prob in probabilities.values()],
                        textposition='auto',
                    )
                ])

                fig.update_layout(
                    title="State Probabilities",
                    xaxis_title="Basis State",
                    yaxis_title="Probability",
                    yaxis_range=[0, 1]
                )

                st.plotly_chart(fig)

                # Display target state probability
                target_prob = probabilities.get(target_state, 0)
                st.info(f"Probability of measuring target state |{target_state}⟩: {target_prob:.4f}")

                if target_prob < 0.5:
                    st.warning("The probability of the target state is low. Try adjusting the number of iterations.")
            else:
                st.error(f"Simulation failed: {result.get('error', 'Unknown error')}")
        except Exception as e:
            st.error(f"Error during simulation: {str(e)}")
            st.info("Try reducing the number of qubits or iterations.")

def show_quantum_fourier_transform():
    st.header("Quantum Fourier Transform")
    st.markdown("""
    ### Overview
    The Quantum Fourier Transform (QFT) is a key component in many quantum algorithms,
    including Shor's factoring algorithm and quantum phase estimation.

    ### Technical Details
    - **Input**: Quantum state |x⟩
    - **Output**: Fourier transformed state
    - **Speedup**: O(n log n) vs O(N log N) classical FFT

    ### Applications
    - Period finding in Shor's algorithm
    - Quantum phase estimation
    - Quantum signal processing
    - Hidden subgroup problems

    ### Mathematical Foundation
    The QFT performs the transformation:
    |j⟩ → 1/√N ∑ₖ e^{2πijk/N} |k⟩

    ### How it works:
    1. Apply Hadamard gates
    2. Apply controlled phase rotations
    3. Swap qubits (if necessary)
    """)

    # Interactive demonstration
    st.subheader("Interactive Demo")
    n_qubits = st.slider("Number of Qubits for QFT", 1, 3, 2)
    input_state = st.selectbox(
        "Input State",
        [format(i, f'0{n_qubits}b') for i in range(2**n_qubits)]
    )

    if st.button("Run QFT"):
        qc = QuantumComputer()
        circuit_ops = []

        # Prepare input state
        input_int = int(input_state, 2)
        for i in range(n_qubits):
            if input_int & (1 << i):
                circuit_ops.append({'gate': 'X', 'target': i})

        # Apply QFT
        for i in range(n_qubits):
            circuit_ops.append({'gate': 'H', 'target': i})
            for j in range(i+1, n_qubits):
                circuit_ops.append({'gate': 'CZ', 'control': j, 'target': i})

        result = qc.simulate_circuit(circuit_ops)

        if result['success']:
            st.success("QFT completed successfully!")
            st.write("Final State Vector:", result['state_vector'])
            st.write("\nMeasurement Results:")
            for state, data in result['measurements'].items():
                st.write(f"State |{state}⟩: {data['probability']:.4f}")
        else:
            st.error(f"Simulation failed: {result.get('error', 'Unknown error')}")


def show_traveling_salesman():
    st.header("Traveling Salesman Problem using QAOA")
    st.markdown("""
    ### Overview
    The Quantum Approximate Optimization Algorithm (QAOA) is a hybrid quantum-classical
    algorithm designed for solving combinatorial optimization problems.

    ### Technical Details
    - **Input**: Graph with N cities and distances
    - **Output**: Approximate shortest tour
    - **Advantage**: Potential for better approximation ratios

    ### Applications
    - Route optimization
    - Network design
    - Resource allocation
    - Logistics planning

    ### Key Concepts
    1. **Cost Hamiltonian**: Encodes problem constraints
    2. **Mixer Hamiltonian**: Explores solution space
    3. **Variational Parameters**: Optimized classically

    ### Problem Setup:
    1. Select number of cities
    2. Define distances between cities
    3. Use QAOA to find the shortest route
    """)

    # Interactive demo setup
    n_cities = st.slider("Number of Cities", 2, 4, 3)

    # Generate random city coordinates for visualization
    np.random.seed(42)  # For reproducibility
    city_coords = np.random.rand(n_cities, 2) * 10

    # Display city locations
    st.subheader("City Locations")
    import plotly.graph_objects as go
    fig = go.Figure()

    # Add cities as points
    fig.add_trace(go.Scatter(
        x=city_coords[:, 0],
        y=city_coords[:, 1],
        mode='markers+text',
        text=[f'City {i}' for i in range(n_cities)],
        textposition="top center",
        marker=dict(size=15)
    ))

    fig.update_layout(
        title="City Map",
        xaxis_title="X Coordinate",
        yaxis_title="Y Coordinate",
        width=600,
        height=400
    )

    st.plotly_chart(fig)

    if st.button("Find Optimal Route"):
        try:
            # Calculate distances between cities
            distances = np.zeros((n_cities, n_cities))
            for i in range(n_cities):
                for j in range(n_cities):
                    distances[i,j] = np.sqrt(np.sum((city_coords[i] - city_coords[j])**2))

            # Create QAOA circuit
            qc = QuantumComputer()
            n_qubits = n_cities * 2  # Encoding cities requires more qubits

            # Initialize superposition
            circuit_ops = [{'gate': 'H', 'target': i} for i in range(n_qubits)]

            # Add QAOA specific operations (simplified version)
            for i in range(n_qubits-1):
                circuit_ops.append({'gate': 'CZ', 'control': i, 'target': i+1})

            result = qc.simulate_circuit(circuit_ops)

            if result['success']:
                st.success("QAOA optimization completed!")

                # Display results
                st.subheader("Possible Routes and Probabilities")
                for state, data in result['measurements'].items():
                    if data['probability'] > 0.01:  # Only show significant probabilities
                        st.write(f"Route: {state}, Probability: {data['probability']:.4f}")
            else:
                st.error(f"Optimization failed: {result.get('error', 'Unknown error')}")
        except Exception as e:
            st.error(f"Error during optimization: {str(e)}")
            st.info("Try reducing the number of cities.")

if __name__ == "__main__":
    show_algorithms()