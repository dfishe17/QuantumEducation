import streamlit as st
import plotly.graph_objects as go
import numpy as np

def create_circuit_heatmap(circuit_ops, performance_data):
    """
    Create a heat map visualization of quantum circuit performance.
    
    Args:
        circuit_ops: List of circuit operations
        performance_data: Dictionary containing performance metrics
    """
    # Extract gate types and qubit indices
    n_qubits = max([op.get('target', 0) for op in circuit_ops]) + 1
    n_steps = len(circuit_ops)
    
    # Initialize performance matrix
    perf_matrix = np.zeros((n_qubits, n_steps))
    gate_labels = []
    
    # Populate performance matrix
    for i, op in enumerate(circuit_ops):
        gate = op['gate']
        target = op.get('target', 0)
        control = op.get('control', None)
        
        # Set performance value based on gate type
        perf_value = performance_data.get(f"step_{i}", {}).get('fidelity', 0.5)
        perf_matrix[target, i] = perf_value
        
        # For two-qubit gates, also mark the control qubit
        if control is not None:
            perf_matrix[control, i] = perf_value
        
        gate_labels.append(gate)
    
    # Create heat map
    fig = go.Figure(data=go.Heatmap(
        z=perf_matrix,
        x=[f"Step {i+1}\n{gate}" for i, gate in enumerate(gate_labels)],
        y=[f"Qubit {i}" for i in range(n_qubits)],
        colorscale='RdYlBu',
        zmin=0,
        zmax=1,
        text=[[f"Fidelity: {perf_matrix[i,j]:.3f}" for j in range(n_steps)] for i in range(n_qubits)],
        hoverongaps=False
    ))
    
    fig.update_layout(
        title="Circuit Performance Heat Map",
        xaxis_title="Circuit Steps",
        yaxis_title="Qubits",
        width=800,
        height=400
    )
    
    return fig

def show_performance_metrics(performance_data):
    """Display additional performance metrics."""
    st.subheader("Performance Metrics")
    
    if performance_data:
        metrics = st.columns(3)
        
        with metrics[0]:
            avg_fidelity = np.mean([step.get('fidelity', 0) 
                                  for step in performance_data.values()])
            st.metric("Average Fidelity", f"{avg_fidelity:.3f}")
        
        with metrics[1]:
            total_time = sum(step.get('time', 0) 
                           for step in performance_data.values())
            st.metric("Total Execution Time", f"{total_time:.2f} ms")
        
        with metrics[2]:
            n_gates = len(performance_data)
            st.metric("Total Gates", n_gates)
