import streamlit as st
import plotly.graph_objects as go
import numpy as np
from quantum_utils import calculate_bloch_coordinates

def show_state_visualizer():
    st.title("Quantum State Visualization")
    
    # State input
    st.subheader("Define Quantum State")
    alpha = st.slider("α (amplitude of |0⟩)", 0.0, 1.0, 0.7071, step=0.0001)
    beta_magnitude = np.sqrt(1 - alpha**2)
    beta_phase = st.slider("β phase (radians)", 0.0, 2*np.pi, 0.0, step=0.01)
    
    # Display current values
    st.write(f"Current values:")
    st.write(f"α = {alpha:.4f}")
    st.write(f"β magnitude = {beta_magnitude:.4f}")
    beta = beta_magnitude * np.exp(1j * beta_phase)
    
    # Create state vector
    state_vector = np.array([alpha, beta])
    
    # Display state vector
    st.write("State Vector:", state_vector)
    
    # Visualize on Bloch sphere
    bloch_sphere = create_bloch_sphere(state_vector)
    st.plotly_chart(bloch_sphere)

def create_bloch_sphere(state_vector):
    """Create an interactive Bloch sphere visualization."""
    # Calculate Bloch coordinates
    x, y, z = calculate_bloch_coordinates(state_vector)
    
    # Create sphere
    phi = np.linspace(0, 2*np.pi, 100)
    theta = np.linspace(0, np.pi, 100)
    phi, theta = np.meshgrid(phi, theta)
    
    x_sphere = np.sin(theta) * np.cos(phi)
    y_sphere = np.sin(theta) * np.sin(phi)
    z_sphere = np.cos(theta)
    
    fig = go.Figure()
    
    # Add sphere surface
    fig.add_trace(go.Surface(
        x=x_sphere, y=y_sphere, z=z_sphere,
        opacity=0.3,
        showscale=False
    ))
    
    # Add state vector
    fig.add_trace(go.Scatter3d(
        x=[0, x], y=[0, y], z=[0, z],
        mode='lines+markers',
        line=dict(color='red', width=5),
        marker=dict(size=5, color='red')
    ))
    
    # Update layout
    fig.update_layout(
        title="Bloch Sphere Representation",
        width=600,
        height=600,
        scene=dict(
            xaxis_title="X",
            yaxis_title="Y",
            zaxis_title="Z",
            aspectmode='cube'
        )
    )
    
    return fig
