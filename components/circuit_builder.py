import streamlit as st
import plotly.graph_objects as go
import numpy as np
from quantum_utils import QuantumComputer
from components.circuit_heatmap import create_circuit_heatmap, show_performance_metrics

def show_circuit_builder():
    st.title("Quantum Circuit Builder")

    # Initialize quantum computer
    qc = QuantumComputer()
    available_gates = qc.get_available_gates()

    # Circuit building interface
    st.subheader("Build Your Circuit")

    # Number of qubits selector
    num_qubits = st.slider("Number of Qubits", 1, 3, 1)

    # Circuit operations with state tracking
    circuit_ops = []

    # Show current circuit state
    if 'circuit_ops' not in st.session_state:
        st.session_state.circuit_ops = []

    st.write("Current Circuit State:")
    if not st.session_state.circuit_ops:
        st.info("Circuit is empty. Add gates using the controls below.")

    # Initialize quantum computer instance
    qc = QuantumComputer()

    # Display available gates with descriptions
    st.subheader("Available Gates")
    for gate, description in qc.gate_descriptions.items():
        st.markdown(f"**{gate}**: {description}")

    # Gate selection for each qubit with improved layout
    st.subheader("Circuit Construction")
    for i in range(num_qubits):
        st.markdown(f"#### Qubit {i}")
        col1, col2 = st.columns([3, 1])

        with col1:
            # Single qubit gates
            gates = st.multiselect(
                f"Select gates for Qubit {i}",
                [g for g in available_gates if g not in ['CNOT', 'CZ']],
                key=f"qubit_{i}"
            )

            for gate in gates:
                try:
                    new_op = {
                        'gate': gate,
                        'target': i
                    }
                    circuit_ops.append(new_op)
                    st.success(f"Added {gate} gate to qubit {i}")
                except Exception as e:
                    st.error(f"Failed to add gate: {str(e)}")

        with col2:
            # Two-qubit gates
            if num_qubits > 1:
                control_gates = st.multiselect(
                    f"Control gates from Qubit {i}",
                    ['CNOT', 'CZ'],
                    key=f"control_{i}"
                )

                for gate in control_gates:
                    target_options = [j for j in range(num_qubits) if j != i]
                    target = st.selectbox(
                        f"Target for {gate}",
                        target_options,
                        key=f"target_{i}_{gate}"
                    )
                    circuit_ops.append({
                        'gate': gate,
                        'control': i,
                        'target': target
                    })

    # Circuit visualization with enhanced features
    if st.button("Visualize Circuit"):
        fig = create_circuit_diagram(circuit_ops, num_qubits)
        st.plotly_chart(fig)

        # Add circuit complexity analysis
        st.subheader("Circuit Complexity Analysis")
        analyze_circuit_complexity(circuit_ops)

    # Run circuit simulation with advanced analysis
    if st.button("Run Circuit"):
        if not circuit_ops:
            st.warning("Please add some gates to your circuit before running the simulation.")
            return

        with st.spinner("Running quantum circuit simulation..."):
            result = qc.simulate_circuit(circuit_ops)

            if result['success']:
                st.success("Simulation completed successfully!")

                # Show performance visualization
                if 'performance_data' in result:
                    st.subheader("Circuit Performance Analysis")
                    heatmap = create_circuit_heatmap(circuit_ops, result['performance_data'])
                    st.plotly_chart(heatmap)
                    show_performance_metrics(result['performance_data'])

                st.subheader("Simulation Results")
                # Display state vector with enhanced visualization
                st.write("Final State Vector:")
                state_vector = result['state_vector']
                # Create columns for better layout
                cols = st.columns(2)
                with cols[0]:
                    st.write("State")
                with cols[1]:
                    st.write("Amplitude")
                for i, amplitude in enumerate(state_vector):
                    with cols[0]:
                        st.write(f"|{format(i, f'0{num_qubits}b')}⟩")
                    with cols[1]:
                        # Format complex numbers properly
                        if isinstance(amplitude, complex):
                            st.write(f"{amplitude.real:.3f}{amplitude.imag:+.3f}j")
                        else:
                            st.write(f"{amplitude:.3f}")

                # Display measurement results with improved formatting
                st.write("\nMeasurement Results:")
                measurements = result['measurements']

                # Create a table for measurements
                cols = st.columns([2, 1, 1, 1])
                cols[0].write("Basis State")
                cols[1].write("Counts")
                cols[2].write("Probability")
                cols[3].write("Visualization")

                for state, data in measurements.items():
                    cols = st.columns([2, 1, 1, 1])
                    cols[0].write(data['basis_state'])
                    cols[1].write(f"{data['count']}/1000")
                    cols[2].write(f"{data['probability']:.4f}")
                    cols[3].progress(data['probability'])

                # Add circuit optimization suggestions
                show_optimization_suggestions(circuit_ops)
            else:
                st.error(f"Simulation failed: {result.get('error', 'Unknown error')}")
                st.info("Try simplifying your circuit or checking the gate connections.")

def analyze_circuit_complexity(circuit_ops):
    """Analyze and display circuit complexity metrics."""
    # Calculate basic metrics
    n_gates = len(circuit_ops)
    n_two_qubit_gates = sum(1 for op in circuit_ops if 'control' in op)

    # Display metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Gates", n_gates)
    with col2:
        st.metric("Two-Qubit Gates", n_two_qubit_gates)
    with col3:
        st.metric("Circuit Depth", n_gates)

    # Add complexity warning if needed
    if n_gates > 10:
        st.warning("Circuit complexity is high. Consider optimization.")

def show_optimization_suggestions(circuit_ops):
    """Display suggestions for circuit optimization."""
    st.subheader("Optimization Suggestions")

    # Check for common patterns that could be optimized
    consecutive_same_gates = False
    for i in range(len(circuit_ops)-1):
        if (circuit_ops[i].get('gate') == circuit_ops[i+1].get('gate') and 
            circuit_ops[i].get('target') == circuit_ops[i+1].get('target')):
            consecutive_same_gates = True
            break

    if consecutive_same_gates:
        st.info("Found consecutive identical gates. These might cancel out.")

    # Additional optimization tips
    st.markdown("""
    ### Optimization Tips:
    1. **Gate Cancellation**: Look for pairs of gates that cancel each other
    2. **Circuit Depth**: Try to parallelize operations where possible
    3. **Two-Qubit Gates**: Minimize the number of CNOT/CZ gates
    4. **Measurement Strategy**: Consider measuring only necessary qubits
    """)

def create_circuit_diagram(circuit_ops, num_qubits):
    """Create a visual representation of the quantum circuit."""
    fig = go.Figure()

    # Add qubit lines
    for i in range(num_qubits):
        fig.add_trace(go.Scatter(
            x=[0, 10],
            y=[i, i],
            mode='lines',
            line=dict(color='black'),
            name=f'Qubit {i}'
        ))

    # Add gates and connections
    for j, op in enumerate(circuit_ops):
        x_pos = j + 1
        gate = op['gate']
        target = op['target']

        if gate in ['CNOT', 'CZ']:
            # Draw control point
            control = op['control']
            fig.add_trace(go.Scatter(
                x=[x_pos],
                y=[control],
                mode='markers',
                marker=dict(size=10, color='black'),
                name=f'Control {j}'
            ))

            # Draw target gate
            symbol = '⊕' if gate == 'CNOT' else 'Z'
            fig.add_trace(go.Scatter(
                x=[x_pos],
                y=[target],
                mode='markers+text',
                text=[symbol],
                textposition="middle center",
                marker=dict(size=30, color='white', line=dict(color='black', width=2)),
                name=f'{gate} Target {j}'
            ))

            # Draw connecting line
            y_coords = sorted([control, target])
            fig.add_trace(go.Scatter(
                x=[x_pos, x_pos],
                y=y_coords,
                mode='lines',
                line=dict(color='black'),
                name=f'Connection {j}'
            ))
        else:
            # Draw single qubit gate
            fig.add_trace(go.Scatter(
                x=[x_pos],
                y=[target],
                mode='markers+text',
                text=[gate],
                textposition="middle center",
                marker=dict(size=30, color='lightblue', line=dict(color='black', width=1)),
                name=f'{gate} Gate {j}'
            ))

    fig.update_layout(
        showlegend=False,
        xaxis=dict(showgrid=False, range=[-0.5, 11]),
        yaxis=dict(showgrid=False, range=[-0.5, num_qubits-0.5]),
        plot_bgcolor='white',
        height=100 + 100*num_qubits
    )

    return fig