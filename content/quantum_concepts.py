import streamlit as st
import logging
from components.progress_tracker import mark_complete, is_topic_completed
from content.quizzes import show_quiz
from io import BytesIO
import base64
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def show_tooltip(term, explanation):
    """Display a tooltip using Streamlit's help parameter"""
    try:
        logger.debug(f"Showing tooltip for term: {term}")
        return st.markdown(f"{term}", help=explanation)
    except Exception as e:
        logger.error(f"Error showing tooltip for {term}: {str(e)}")
        return term

def show_learn_more_button(title, content):
    """Create an expandable section using Streamlit's expander"""
    try:
        logger.debug(f"Creating Learn More section for: {title}")
        with st.expander(f"🔍 Learn More: {title}"):
            st.markdown(content, unsafe_allow_html=True)
        logger.info(f"Created Learn More section for: {title}")
    except Exception as e:
        logger.error(f"Error in show_learn_more_button for {title}: {str(e)}")
        st.error("There was an error displaying this content. Please refresh the page.")

def show_qubit_advanced_content():
    try:
        with st.expander("🎓 Advanced Qubit Theory"):
            st.markdown("""
            <div class="card">
                <div class="card-title">🧬 Advanced Qubit Concepts</div>
                <div class="card-content">
                    <div class="implementation-grid">
                        <div class="impl-card">
                            <div class="impl-title">🔄 Mixed States</div>
                            <ul>
                                <li>Density matrix formalism</li>
                                <li>Partial trace operations</li>
                                <li>Quantum channels</li>
                                <li>Decoherence effects</li>
                            </ul>
                        </div>
                        <div class="impl-card">
                            <div class="impl-title">🌟 Advanced Properties</div>
                            <ul>
                                <li>No-deletion theorem</li>
                                <li>Quantum discord</li>
                                <li>Contextuality</li>
                                <li>Non-locality</li>
                            </ul>
                        </div>
                        <div class="impl-card">
                            <div class="impl-title">📊 Error Analysis</div>
                            <ul>
                                <li>Coherence time</li>
                                <li>Gate fidelity</li>
                                <li>State preparation errors</li>
                                <li>Measurement accuracy</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        logger.error(f"Error in show_qubit_advanced_content: {str(e)}")
        st.error("An error occurred while displaying advanced qubit content. Please refresh the page.")

def show_gates_advanced_content():
    try:
        with st.expander("🎯 Advanced Gate Operations"):
            st.markdown("""
            <div class="card">
                <div class="card-title">🔬 Advanced Gate Theory</div>
                <div class="card-content">
                    <div class="implementation-grid">
                        <div class="impl-card">
                            <div class="impl-title">🌀 Continuous Operations</div>
                            <ul>
                                <li>Hamiltonian evolution</li>
                                <li>Adiabatic processes</li>
                                <li>Quantum optimal control</li>
                                <li>Composite pulses</li>
                            </ul>
                        </div>
                        <div class="impl-card">
                            <div class="impl-title">🧮 Advanced Decompositions</div>
                            <ul>
                                <li>Solovay-Kitaev theorem</li>
                                <li>Cartan decomposition</li>
                                <li>Quantum Shannon decomposition</li>
                                <li>Gate synthesis algorithms</li>
                            </ul>
                        </div>
                        <div class="impl-card">
                            <div class="impl-title">⚡ Physical Implementation</div>
                            <ul>
                                <li>Microwave pulses</li>
                                <li>Laser control</li>
                                <li>Magnetic fields</li>
                                <li>Exchange interactions</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        logger.error(f"Error in show_gates_advanced_content: {str(e)}")
        st.error("An error occurred while displaying advanced gate content. Please refresh the page.")

def show_circuits_advanced_content():
    try:
        with st.expander("🔌 Advanced Circuit Theory"):
            st.markdown("""
            <div class="card">
                <div class="card-title">📚 Advanced Circuit Concepts</div>
                <div class="card-content">
                    <div class="implementation-grid">
                        <div class="impl-card">
                            <div class="impl-title">🎭 Fault Tolerance</div>
                            <ul>
                                <li>Error correcting codes</li>
                                <li>Threshold theorem</li>
                                <li>Surface codes</li>
                                <li>Magic state distillation</li>
                            </ul>
                        </div>
                        <div class="impl-card">
                            <div class="impl-title">🔄 Advanced Compilation</div>
                            <ul>
                                <li>Circuit optimization</li>
                                <li>Qubit routing</li>
                                <li>Resource estimation</li>
                                <li>Noise-aware compilation</li>
                            </ul>
                        </div>
                        <div class="impl-card">
                            <div class="impl-title">📊 Performance Analysis</div>
                            <ul>
                                <li>Circuit metrics</li>
                                <li>Simulation techniques</li>
                                <li>Verification methods</li>
                                <li>Benchmarking protocols</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        logger.error(f"Error in show_circuits_advanced_content: {str(e)}")
        st.error("An error occurred while displaying advanced circuit content. Please refresh the page.")

def show_measurements_advanced_content():
    try:
        with st.expander("📏 Advanced Measurement Theory"):
            st.markdown("""
            <div class="card">
                <div class="card-title">🔬 Advanced Measurement Concepts</div>
                <div class="card-content">
                    <div class="implementation-grid">
                        <div class="impl-card">
                            <div class="impl-title">🎯 Quantum Estimation</div>
                            <ul>
                                <li>Parameter estimation</li>
                                <li>Fisher information</li>
                                <li>Quantum Cramér-Rao bound</li>
                                <li>Adaptive protocols</li>
                            </ul>
                        </div>
                        <div class="impl-card">
                            <div class="impl-title">🔄 Advanced Protocols</div>
                            <ul>
                                <li>Quantum non-demolition</li>
                                <li>Continuous measurement</li>
                                <li>Heralded measurements</li>
                                <li>Entanglement witnesses</li>
                            </ul>
                        </div>
                        <div class="impl-card">
                            <div class="impl-title">📊 Error Characterization</div>
                            <ul>
                                <li>Readout error mitigation</li>
                                <li>Cross-talk analysis</li>
                                <li>Calibration methods</li>
                                <li>State validation</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        logger.error(f"Error in show_measurements_advanced_content: {str(e)}")
        st.error("An error occurred while displaying advanced measurement content. Please refresh the page.")


def show_qubit_content():
    logger.info("Displaying qubit content")
    try:
        st.header("Qubits: The Building Blocks of Quantum Computing")
        st.markdown("""
        <div class="card">
            <div class="card-title">⚛️ Introduction to Qubits</div>
            <div class="card-content">
            A qubit (quantum bit) is the fundamental unit of quantum information, representing the quantum analog of a classical bit. 
            Unlike classical bits which can only be in state 0 or 1, qubits can exist in a superposition of both states simultaneously.
            This unique property makes quantum computing exponentially more powerful than classical computing for certain tasks.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <div class="card-title">📚 Historical Background</div>
            <div class="card-content">
                <p>The concept of qubits emerged from:</p>
                <ul>
                    <li>1980s: Richard Feynman's proposal of quantum computers</li>
                    <li>1994: Peter Shor's quantum factoring algorithm</li>
                    <li>1996: First experimental demonstration of a qubit</li>
                    <li>2000s: Development of various qubit implementations</li>
                    <li>2020s: Achievement of quantum supremacy</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.subheader("Key Properties of Qubits")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            <div class="feature-card">
                <div class="feature-title">🌊 Superposition</div>
                <ul>
                    <li>Exist in multiple states simultaneously</li>
                    <li>Process multiple possibilities at once</li>
                    <li>Collapses upon measurement</li>
                    <li>Enables quantum parallelism</li>
                    <li>Key to quantum speedup</li>
                    <li>Requires careful state preparation</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="feature-card">
                <div class="feature-title">🔄 Phase</div>
                <ul>
                    <li>Complex number property</li>
                    <li>Determines interference patterns</li>
                    <li>Crucial for algorithms</li>
                    <li>Enables quantum walks</li>
                    <li>Controls quantum gates</li>
                    <li>Affects measurement outcomes</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <div class="feature-card">
                <div class="feature-title">🔗 Entanglement</div>
                <ul>
                    <li>Non-local correlations</li>
                    <li>Einstein's "spooky action"</li>
                    <li>Enables quantum teleportation</li>
                    <li>Powers quantum cryptography</li>
                    <li>Creates quantum networks</li>
                    <li>Fundamental to error correction</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <div class="card-title">🌐 The Bloch Sphere</div>
            <div class="card-content">
                <p>The Bloch sphere is a geometric representation of a qubit's state space:</p>
                <ul>
                    <li>North pole represents |0⟩</li>
                    <li>South pole represents |1⟩</li>
                    <li>Equator represents equal superpositions</li>
                    <li>Surface points represent pure states</li>
                    <li>Interior points represent mixed states</li>
                    <li>Quantum gates are rotations</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <div class="card-title">📐 Mathematical Representation</div>
            <div class="card-content">
                <p>A qubit state can be written as:</p>
                <div class="math-box">
                    |ψ⟩ = α|0⟩ + β|1⟩
                </div>
                <p>where:</p>
                <ul>
                    <li>α and β are complex numbers</li>
                    <li>|α|² + |β|² = 1 (normalization)</li>
                    <li>|α|² is probability of measuring |0⟩</li>
                    <li>|β|² is probability of measuring |1⟩</li>
                </ul>
                <p>Advanced mathematical concepts:</p>
                <ul>
                    <li>Density matrices for mixed states</li>
                    <li>Pauli matrices as measurement bases</li>
                    <li>Quantum operations as unitary matrices</li>
                    <li>Tensor products for multi-qubit systems</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <div class="card-title">🔧 Physical Implementations</div>
            <div class="card-content">
                <div class="implementation-grid">
                    <div class="impl-card">
                        <div class="impl-title">💫 Superconducting Qubits</div>
                        <div class="impl-subtitle">Used by IBM and Google</div>
                        <ul>
                            <li>Based on Josephson junctions</li>
                            <li>Operates at mK temperatures</li>
                            <li>Fast gate operations</li>
                            <li>Good scalability potential</li>
                        </ul>
                    </div>
                    <div class="impl-card">
                        <div class="impl-title">⚡ Trapped Ions</div>
                        <div class="impl-subtitle">Used by IonQ and Honeywell</div>
                        <ul>
                            <li>Individual atoms in EM fields</li>
                            <li>Long coherence times</li>
                            <li>High-fidelity gates</li>
                            <li>All-to-all connectivity</li>
                        </ul>
                    </div>
                    <div class="impl-card">
                        <div class="impl-title">💡 Photonic Qubits</div>
                        <div class="impl-subtitle">Used in optical quantum computers</div>
                        <ul>
                            <li>Room temperature operation</li>
                            <li>Natural for communication</li>
                            <li>Low decoherence</li>
                            <li>Challenging to scale</li>
                        </ul>
                    </div>
                    <div class="impl-card">
                        <div class="impl-title">🔷 Quantum Dots</div>
                        <div class="impl-subtitle">Semiconductor-based qubits</div>
                        <ul>
                            <li>Silicon-based technology</li>
                            <li>CMOS compatible</li>
                            <li>Potential for scaling</li>
                            <li>Industrial fabrication</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <div class="card-title">🎯 Applications and Use Cases</div>
            <div class="card-content">
                <div class="implementation-grid">
                    <div class="impl-card">
                        <div class="impl-title">🔐 Quantum Cryptography</div>
                        <ul>
                            <li>Quantum key distribution</li>
                            <li>Post-quantum cryptography</li>
                            <li>Quantum random numbers</li>
                        </ul>
                    </div>
                    <div class="impl-card">
                        <div class="impl-title">💊 Quantum Chemistry</div>
                        <ul>
                            <li>Molecular simulations</li>
                            <li>Drug discovery</li>
                            <li>Material design</li>
                        </ul>
                    </div>
                    <div class="impl-card">
                        <div class="impl-title">📈 Financial Modeling</div>
                        <ul>
                            <li>Portfolio optimization</li>
                            <li>Risk analysis</li>
                            <li>Market simulation</li>
                        </ul>
                    </div>
                    <div class="impl-card">
                        <div class="impl-title">🧬 Machine Learning</div>
                        <ul>
                            <li>Quantum neural networks</li>
                            <li>Pattern recognition</li>
                            <li>Data classification</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <div class="card-title">🔮 Challenges and Future Directions</div>
            <div class="card-content">
                <div class="implementation-grid">
                    <div class="impl-card">
                        <div class="impl-title">⚠️ Current Challenges</div>
                        <ul>
                            <li>Decoherence</li>
                            <li>Error rates</li>
                            <li>Scalability issues</li>
                            <li>Cost and complexity</li>
                        </ul>
                    </div>
                    <div class="impl-card">
                        <div class="impl-title">🔬 Research Areas</div>
                        <ul>
                            <li>Error correction</li>
                            <li>New qubit types</li>
                            <li>Control systems</li>
                            <li>Quantum memory</li>
                        </ul>
                    </div>
                    <div class="impl-card">
                        <div class="impl-title">🎯 Goals</div>
                        <ul>
                            <li>Million-qubit systems</li>
                            <li>Room temperature operation</li>
                            <li>Quantum internet</li>
                            <li>Fault tolerance</li>
                        </ul>
                    </div>
                    <div class="impl-card">
                        <div class="impl-title">💡 Innovations</div>
                        <ul>
                            <li>Hybrid computing</li>
                            <li>Topological qubits</li>
                            <li>Quantum repeaters</li>
                            <li>New algorithms</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="example-card">
            <div class="example-title">Common Qubit States</div>
            <div class="state-grid">
                <div class="state-item">
                    <div class="state-name">|0⟩ state (Computational Basis)</div>
                    <div class="state-value">α = 1, β = 0</div>
                    <div class="state-note">Classical bit 0</div>
                </div>
                <div class="state-item">
                    <div class="state-name">|1⟩ state (Computational Basis)</div>
                    <div class="state-value">α = 0, β = 1</div>
                    <div class="state-note">Classical bit 1</div>
                </div>
                <div class="state-item">
                    <div class="state-name">|+⟩ state (Hadamard Basis)</div>
                    <div class="state-value">α = 1/√2, β = 1/√2</div>
                    <div class="state-note">Equal superposition</div>
                </div>
                <div class="state-item">
                    <div class="state-name">|-⟩ state (Hadamard Basis)</div>
                    <div class="state-value">α = 1/√2, β = -1/√2</div>
                    <div class="state-note">Equal superposition with phase</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        show_qubit_advanced_content()
        # Add Quiz section


        if st.button("Mark as Complete"):
            mark_complete('concepts', 'Qubits')
            st.success("✅ Topic marked as complete!")
    except Exception as e:
        logger.error(f"Error in show_qubit_content: {str(e)}")
        st.error("An error occurred while displaying qubit content. Please refresh the page.")



def show_gate_fundamental_properties():
    try:
        with st.expander("🔄 Fundamental Properties of Quantum Gates"):
            st.markdown("""
            <div class="card">
                <div class="card-content">
                    <div class="implementation-grid">
                        <div class="impl-card">
                            <div class="impl-title">🔄 Unitarity</div>
                            <p>A fundamental property ensuring quantum information preservation:</p>
                            <ul>
                                <li>Mathematical definition: U†U = UU† = I</li>
                                <li>Preserves state normalization</li>
                                <li>Maintains quantum coherence</li>
                                <li>Ensures reversibility of operations</li>
                            </ul>
                            <div class="math-box">
                                For a unitary matrix U:
                                U†U = I = [1 0]
                                             [0 1]
                            </div>
                        </div>
                        <div class="impl-card">
                            <div class="impl-title">↩️ Reversibility</div>
                            <p>Quantum gates are inherently reversible:</p>
                            <ul>
                                <li>Every gate has an inverse operation</li>
                                <li>Information is preserved</li>
                                <li>Enables quantum error correction</li>
                                <li>Required for quantum algorithms</li>
                            </ul>
                            <div class="math-box">
                                For gate U:
                                UU† = U†U = I
                            </div>
                        </div>
                        <div class="impl-card">
                            <div class="impl-title">🌀 Quantum Properties</div>
                            <p>Special quantum mechanical features:</p>
                            <ul>
                                <li>Superposition preservation</li>
                                <li>Entanglement generation</li>
                                <li>Phase manipulation</li>
                                <li>No-cloning theorem compliance</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        logger.error(f"Error in show_gate_fundamental_properties: {str(e)}")
        st.error("An error occurred while displaying fundamental gate properties. Please refresh the page.")



def show_single_qubit_gates():
    try:
        with st.expander("⚛️ Single-Qubit Gates in Detail"):
            st.markdown("""
            <div class="card">
                <div class="card-content">
                    <div class="gate-grid">
                        <div class="gate-card">
                            <div class="gate-symbol">X</div>
                            <div class="gate-title">Pauli-X Gate (NOT)</div>
                            <div class="gate-matrix">
                                [0 1]
                                [1 0]
                            </div>
                            <p>Effects:</p>
                            <ul>
                                <li>Flips |0⟩ to |1⟩ and vice versa</li>
                                <li>Classical NOT operation</li>
                                <li>π rotation around X-axis</li>
                            </ul>
                        </div>
                        <div class="gate-card">
                            <div class="gate-symbol">H</div>
                            <div class="gate-title">Hadamard Gate</div>
                            <div class="gate-matrix">
                                [1  1]
                                [1 -1] / √2
                            </div>
                            <p>Effects:</p>
                            <ul>
                                <li>Creates equal superposition</li>
                                <li>Maps between X and Z bases</li>
                                <li>Self-inverse operation</li>
                            </ul>
                        </div>
                        <div class="gate-card">
                            <div class="gate-symbol">Z</div>
                            <div class="gate-title">Pauli-Z Gate</div>
                            <div class="gate-matrix">
                                [1  0]
                                [0 -1]
                            </div>
                            <p>Effects:</p>
                            <ul>
                                <li>Phase flip on |1⟩</li>
                                <li>π rotation around Z-axis</li>
                                <li>Leaves |0⟩ unchanged</li>
                            </ul>
                        </div>
                        <div class="gate-card">
                            <div class="gate-symbol">Y</div>
                            <div class="gate-title">Pauli-Y Gate</div>
                            <div class="gate-matrix">
                                [0 -i]
                                [i  0]
                            </div>
                            <p>Effects:</p>
                            <ul>
                                <li>Complex rotation</li>
                                <li>π rotation around Y-axis</li>
                                <li>Combination of X and Z</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        logger.error(f"Error in show_single_qubit_gates: {str(e)}")
        st.error("An error occurred while displaying single-qubit gates. Please refresh the page.")



def show_multi_qubit_gates():
    try:
        with st.expander("🔗 Multi-Qubit Gates Explained"):
            st.markdown("""
            <div class="card">
                <div class="card-content">
                    <div class="multi-gate-section">
                        <div class="gate-explanation">
                            <h3>CNOT (Controlled-NOT)</h3>
                            <p>The fundamental two-qubit gate:</p>
                            <ul>
                                <li>Control qubit determines operation</li>
                                <li>Creates entanglement between qubits</li>
                                <li>Essential for quantum algorithms</li>
                                <li>Building block for error correction</li>
                            </ul>
                            <div class="gate-matrix-large">
                                Matrix representation:
                                [1 0 0 0]
                                [0 1 0 0]
                                [0 0 0 1]
                                [0 0 1 0]
                            </div>
                        </div>
                        <div class="gate-truth-table">
                            <h4>CNOT Truth Table</h4>
                            <table>
                                <tr><th>Input</th><th>Output</th><th>Action</th></tr>
                                <tr><td>|00⟩</td><td>|00⟩</td><td>No change</td></tr>
                                <tr><td>|01⟩</td><td>|01⟩</td><td>No change</td></tr>
                                <tr><td>|10⟩</td><td>|11⟩</td><td>Flip target</td></tr>
                                <tr><td>|11⟩</td><td>|10⟩</td><td>Flip target</td></tr>
                            </table>
                        </div>
                    </div>
                    <div class="implementation-grid">
                        <div class="impl-card">
                            <div class="impl-title">SWAP Gate</div>
                            <p>Exchanges quantum states:</p>
                            <ul>
                                <li>|ψ₁ψ₂⟩ → |ψ₂ψ₁⟩</li>
                                <li>Composed of three CNOTs</li>
                                <li>Essential for circuit optimization</li>
                            </ul>
                        </div>
                        <div class="impl-card">
                            <div class="impl-title">Controlled-Z (CZ)</div>
                            <p>Phase control operation:</p>
                            <ul>
                                <li>Applies Z gate conditionally</li>
                                <li>Symmetric between qubits</li>
                                <li>Key for phase kickback</li>
                            </ul>
                        </div>
                        <div class="impl-card">
                            <div class="impl-title">Toffoli (CCX)</div>
                            <p>Three-qubit controlled operation:</p>
                            <ul>
                                <li>Universal for classical computing</li>
                                <li>Building block for arithmetic</li>
                                <li>Reversible AND gate</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        logger.error(f"Error in show_multi_qubit_gates: {str(e)}")
        st.error("An error occurred while displaying multi-qubit gates. Please refresh the page.")


def show_advanced_gates():
    try:
        with st.expander("🚀 Advanced Quantum Gates"):
            st.markdown("""
            <div class="card">
                <div class="card-content">
                    <div class="implementation-grid">
                        <div class="impl-card">
                            <div class="impl-title">🔄 Rotation Gates</div>
                            <p>Continuous single-qubit rotations:</p>
                            <ul>
                                <li>Rx(θ): X-axis rotation</li>
                                <li>Ry(θ): Y-axis rotation</li>
                                <li>Rz(θ): Z-axis rotation</li>
                                <li>Arbitrary angle control</li>
                            </ul>
                            <div class="math-box">
                                Rx(θ) = [cos(θ/2)  -i⋅sin(θ/2)]
                                           [-i⋅sin(θ/2)  cos(θ/2)]
                            </div>
                        </div>
                        <div class="impl-card">
                            <div class="impl-title">🎭 Phase Gates</div>
                            <p>Precise phase control:</p>
                            <ul>
                                <li>S Gate: π/2 phase</li>
                                <li>T Gate: π/4 phase</li>
                                <li>P(φ): Arbitrary phase</li>
                                <li>Essential for fault tolerance</li>
                            </ul>
                        </div>
                        <div class="impl-card">
                            <div class="impl-title">🌟 Controlled-Unitary</div>
                            <p>General controlled operations:</p>
                            <ul>
                                <li>Control arbitrary unitaries</li>
                                <li>Phase estimation components</li>
                                <li>Algorithm building blocks</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        logger.error(f"Error in show_advanced_gates: {str(e)}")
        st.error("An error occurred while displaying advanced gates. Please refresh the page.")


def show_gate_applications():
    try:
        with st.expander("💡 Gate Applications and Use Cases"):
            st.markdown("""
            <div class="card">
                <div class="card-content">
                    <div class="application-grid">
                        <div class="app-card">
                            <div class="app-title">🔒 Quantum Cryptography</div>
                            <p>Security Applications:</p>
                            <ul>
                                <li>BB84 Protocol Implementation</li>
                                <li>Key Distribution Schemes</li>
                                <li>Quantum Digital Signatures</li>
                                <li>State Preparation for QKD</li>
                            </ul>
                        </div>
                        <div class="app-card">
                            <div class="app-title">🧮 Quantum Algorithms</div>
                            <p>Algorithm Components:</p>
                            <ul>
                                <li>Quantum Fourier Transform</li>
                                <li>Phase Estimation Circuits</li>
                                <li>Grover's Search Oracle</li>
                                <li>Amplitude Amplification</li>
                            </ul>
                        </div>
                        <div class="app-card">
                            <div class="app-title">🔬 Quantum Simulation</div>
                            <p>Simulation Applications:</p>
                            <ul>
                                <li>Hamiltonian Evolution</li>
                                <li>Molecular Dynamics</li>
                                <li>Quantum Chemistry</li>
                                <li>Material Science</li>
                            </ul>
                        </div>
                        <div class="app-card">
                            <div class="app-title">📊 Error Correction</div>
                            <p>Error Handling:</p>
                            <ul>
                                <li>Stabilizer Measurements</li>
                                <li>Syndrome Detection</li>
                                <li>Quantum Memory Protection</li>
                                <li>Fault-Tolerant Operations</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        logger.error(f"Error in show_gate_applications: {str(e)}")
        st.error("An error occurred while displaying gate applications. Please refresh the page.")


def show_gate_content():
    logger.info("Displaying gate content")
    try:
        st.header("Quantum Gates: Manipulating Quantum States")

        # Introduction section
        st.write("In quantum computing, ", end='')
        show_tooltip("quantum gates", "Fundamental operations that manipulate quantum states, similar to classical logic gates but preserving quantum properties")
        st.write(" are the building blocks of quantum circuits. They perform ", end='')
        show_tooltip("unitary operations", "Mathematical operations that preserve thenorm of quantum states and ensure reversibility")
        st.write(" on qubits, enabling powerful quantum computations.")

        # Fundamental Properties section
        show_gate_fundamental_properties()
        # Basic Gates section with expanded information
        st.markdown("### 🔄 Basic Gates")
        basic_gates_col1, basic_gates_col2, basic_gates_col3 = st.columns(3)

        with basic_gates_col1:
            st.markdown("#### Pauli-X Gate (NOT)")
            st.latex(r'''\begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}''')
            st.markdown("""
            **Effects:**
            - Flips |0⟩ to |1⟩ and vice versa
            - Classical NOT operation
            - π rotation around X-axis

            **Applications:**
            - State inversion
            - Quantum NOT operations
            - Basis state preparation
            """)

        with basic_gates_col2:
            st.markdown("#### Hadamard Gate")
            st.latex(r'''\frac{1}{\sqrt{2}}\begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix}''')
            st.markdown("""
            **Effects:**
            - Creates equal superposition
            - Maps between X and Z bases
            - Self-inverse operation

            **Applications:**
            - Quantum Fourier Transform
            - State initialization
            - Quantum algorithms
            """)

        with basic_gates_col3:
            st.markdown("#### Phase Gate (S)")
            st.latex(r'''\begin{bmatrix} 1 & 0 \\ 0 & i \end{bmatrix}''')
            st.markdown("""
            **Effects:**
            - Adds π/2 phase to |1⟩
            - Leaves |0⟩ unchanged
            - Key for Z-axis rotation

            **Applications:**
            - Phase manipulation
            - Quantum error correction
            - Complex state preparation
            """)

        # Advanced Gates section with more detail
        with st.expander("🚀 Advanced Quantum Gates"):
            st.markdown("### Advanced Quantum Gates")
            st.markdown("""
            Advanced quantum gates enable complex quantum operations and are essential for quantum algorithms.
            """)
            adv_col1, adv_col2 = st.columns(2)

            with adv_col1:
                st.markdown("#### Controlled Gates")
                st.latex(r'''CNOT = \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 1 & 0 \end{bmatrix}''')
                st.markdown("""
                **Types:**
                - CNOT (Controlled-NOT)
                - CZ (Controlled-Z)
                - Controlled-Phase

                **Applications:**
                - Entanglement creation
                - Quantum error correction
                - Multi-qubit operations
                """)

            with adv_col2:
                st.markdown("#### Special Purpose Gates")
                st.markdown("""
                **Rotation Gates:**
                - Rx(θ): X-axis rotation
                - Ry(θ): Y-axis rotation
                - Rz(θ): Z-axis rotation

                **Advanced Operations:**
                - Toffoli (CCNOT)
                - Fredkin (CSWAP)
                - Custom controlled operations
                """)

        # Practical Applications section
        st.markdown("### 🔬 Practical Applications")
        app_col1, app_col2 = st.columns(2)

        with app_col1:
            with st.expander("🔐 Quantum Cryptography"):
                st.markdown("""
                #### Quantum Cryptography Applications
                **Key Distribution:**
                - BB84 protocol implementation
                - E91 protocol
                - Device-independent QKD

                **Security Features:**
                - Quantum key generation
                - Secure state preparation
                - Measurement protocols

                **Advanced Topics:**
                - Authentication schemes
                - Privacy amplification
                - Error correction
                """)

        with app_col2:
            with st.expander("🧮 Quantum Algorithms"):
                st.markdown("""
                #### Algorithm Applications
                **Fundamental Algorithms:**
                - Shor's Algorithm
                  - Integer factorization
                  - Period finding

                **Search Algorithms:**
                - Grover's Search
                  - Database searching
                  - Optimization problems

                **Transform Methods:**
                - Quantum Fourier Transform
                  - Signal processing
                  - Phase estimation
                """)

        # Implementation Challenges
        st.markdown("### 🛠️ Implementation Challenges")
        challenge_col1, challenge_col2 = st.columns(2)

        with challenge_col1:
            st.markdown("""
            #### Physical Limitations
            - Decoherence effects
            - Gate fidelity issues
            - Environmental noise
            - Control precision
            """)

        with challenge_col2:
            st.markdown("""
            #### Technical Challenges
            - Gate calibration
            - Timing constraints
            - Cross-talk effects
            - Quantum error correction
            """)

        # Future Directions
        st.markdown("### 🔮 Future Directions")
        st.markdown("""
        - Development of noise-resilient gates
        - Hardware-efficient gate sets
        - Novel gate implementation methods
        - Optimization of gate sequences
        - Advanced error mitigation techniques
        """)

        # Add Quiz section
        st.markdown("### 📝 Test Your Knowledge")
        if st.button("Take Gates Quiz"):
            show_quiz("gates")
        if st.button("Mark as Complete"):
            mark_complete('concepts', 'Quantum Gates')
            st.success("✅ Topic marked as complete!")

    except Exception as e:
        logger.error(f"Error in show_gate_content: {str(e)}")
        st.error("An error occurred while displaying gate content. Please refresh the page.")



def show_circuit_content():
    logger.info("Displaying quantum circuit content")
    try:
        st.header("Quantum Circuits: Building Quantum Algorithms")
        st.markdown("""
        <div class="card">
            <div class="card-title">🔌 Quantum Circuits</div>
            <div class="card-content">
            Quantum circuits are the frameworks where quantum operations are implemented through a sequence
            of quantum gates. They represent the program that will be executed on a quantum computer.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <div class="card-title">🧩 Circuit Components</div>
            <div class="card-content">
                <div class="implementation-grid">
                    <div class="impl-card">
                        <div class="impl-title">⚡ Initialization</div>
                        <ul>
                            <li>State preparation</li>
                            <li>Qubit reset protocols</li>
                            <li>Ancilla preparation</li>
                            <li>Initial state verification</li>
                        </ul>
                    </div>
                    <div class="impl-card">
                        <div class="impl-title">🔄 Gate Operations</div>
                        <ul>
                            <li>Single-qubit gates</li>
                            <li>Multi-qubit operations</li>
                            <li>Controlled operations</li>
                            <li>Custom gate definitions</li>
                        </ul>
                    </div>
                    <div class="impl-card">
                        <div class="impl-title">📏 Measurements</div>
                        <ul>
                            <li>Basis measurements</li>
                            <li>Partial measurements</li>
                            <li>Error syndrome detection</li>
                            <li>State tomography</li>
                        </ul>
                    </div>
                    <div class="impl-card">
                        <div class="impl-title">⏱️ Timing Control</div>
                        <ul>
                            <li>Circuit barriers</li>
                            <li>Delay operations</li>
                            <li>Synchronization points</li>
                            <li>Parallel execution</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <div class="card-title">📐 Circuit Design Patterns</div>
            <div class="card-content">
                <div class="pattern-grid">
                    <div class="pattern-card">
                        <div class="pattern-title">🔄 State Preparation</div>
                        <div class="pattern-description">Create specific quantum states</div>
                        <div class="pattern-example">
                            H → X → RZ(θ)
                        </div>
                    </div>
                    <div class="pattern-card">
                        <div class="pattern-title">🌊 Quantum Fourier Transform</div>
                        <div class="pattern-description">Change basis for periodicities</div>
                        <div class="pattern-example">
                            H → Phase(θ) → SWAP
                        </div>
                    </div>
                    <div class="pattern-card">
                        <div class="pattern-title">🎯 Amplitude Amplification</div>
                        <div class="pattern-description">Enhance desired states</div>
                        <div class="pattern-example">
                            Oracle → Diffusion
                        </div>
                    </div>
                    <div class="pattern-card">
                        <div class="pattern-title">🔍 Phase Estimation</div>
                        <div class="pattern-description">Extract phase information</div>
                        <div class="pattern-example">
                            H⊗n → CU → QFT†
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <div class="card-title">⚡ Circuit Optimization</div>
            <div class="card-content">
                <div class="optimization-grid">
                    <div class="opt-card">
                        <div class="opt-title">📉 Gate Reduction</div>
                        <ul>
                            <li>Combine adjacent gates</li>
                            <li>Cancel inverse operations</li>
                            <li>Use native gates</li>
                            <li>Remove redundant operations</li>
                        </ul>
                    </div>
                    <div class="opt-card">
                        <div class="opt-title">⏱️ Depth Minimization</div>
                        <ul>
                            <li>Parallel execution</li>
                            <li>Gate commutation rules</li>
                            <li>Layer compression</li>
                            <li>Critical path optimization</li>
                        </ul>
                    </div>
                    <div class="opt-card">
                        <div class="opt-title">🎯 Error Mitigation</div>
                        <ul>
                            <li>Dynamical decoupling</li>
                            <li>Echo sequences</li>
                            <li>Composite pulses</li>
                            <li>Quantum error correction</li>
                        </ul>
                    </div>
                    <div class="opt-card">
                        <div class="opt-title">💻 Hardware Adaptation</div>
                        <ul>
                            <li>Connectivity mapping</li>
                            <li>Noise-aware compilation</li>
                            <li>Calibration optimization</li>
                            <li>Resource estimation</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <div class="card-title">🔧 Hardware Implementation</div>
            <div class="card-content">
                <div class="hardware-grid">
                    <div class="hw-card">
                        <div class="hw-title">📊 Circuit Metrics</div>
                        <div class="metric-item">
                            <span class="metric-name">Depth:</span>
                            <span class="metric-value">Sequential operations</span>
                        </div>
                        <div class="metric-item">
                            <span class="metric-name">Width:</span>
                            <span class="metric-value">Number of qubits</span>
                        </div>
                        <div class="metric-item">
                            <span class="metric-name">Gates:</span>
                            <span class="metric-value">Operation count</span>
                        </div>
                    </div>
                    <div class="hw-card">
                        <div class="hw-title">⚠️ Constraints</div>
                        <ul>
                            <li>Limited connectivity</li>
                            <li>Gate fidelity variations</li>
                            <li>Decoherence times</li>
                            <li>Available operations</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="example-card">
            <div class="example-title">Common Circuit Implementations</div>
            <div class="circuit-grid">
                <div class="circuit-item">
                    <div class="circuit-name">Bell State Preparation</div>
                    <div class="circuit-diagram">
                        q0: ─H─■─
                        q1: ───┼─
                    </div>
                    <div class="circuit-description">
                        Creates maximum entanglement between two qubits
                    </div>
                </div>
                <div class="circuit-item">
                    <div class="circuit-name">Quantum Teleportation</div>
                    <div class="circuit-diagram">
                        q0: ─■─H─M─
                        q1: ─┼─■─M─
                        q2: ─X─Z───
                    </div>
                    <div class="circuit-description">
                        Transfers quantum state using entanglement
                    </div>
                </div>
                <div class="circuit-item">
                    <div class="circuit-name">Grover Iteration</div>
                    <div class="circuit-diagram">
                        ┌Oracle┐┌Diffusion┐
                        ─┤     ├┤         ├─
                        ─┤     ├┤         ├─
                    </div>
                    <div class="circuit-description">
                        Core component of quantum search
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        show_circuits_advanced_content()
        if st.button("Mark as Complete"):
            mark_complete('concepts', 'Quantum Circuits')
            st.success("✅ Topic marked as complete!")
    except Exception as e:
        logger.error(f"Error in show_circuit_content: {str(e)}")
        st.error("An error occurred while displaying circuit content. Please refresh the page.")



def show_measurement_content():
    logger.info("Displaying measurement content")
    try:
        st.header("Quantum Measurements: Extracting Information")
        st.markdown("""
        <div class="card">
            <div class="card-title">📏 Introduction to Quantum Measurements</div>
            <div class="card-content">
            Quantum measurement is the process of extracting classical information from quantum systems.
            It's a fundamental and subtle aspect of quantum mechanics with unique properties and challenges.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <div class="card-title">🎯 Measurement Fundamentals</div>
            <div class="card-content">
                <div class="implementation-grid">
                    <div class="impl-card">
                        <div class="impl-title">📊 Wave Function Collapse</div>
                        <ul>
                            <li>State reduction to eigenstate</li>
                            <li>Probabilistic outcomes</li>
                            <li>No intermediate values</li>
                            <li>Irreversible process</li>
                        </ul>
                    </div>
                    <div class="impl-card">
                        <div class="impl-title">🎲 Born Rule</div>
                        <ul>
                            <li>Probability = |amplitude|²</li>
                            <li>Normalized states</li>
                            <li>Expectation values</li>
                            <li>Statistical predictions</li>
                        </ul>
                    </div>
                    <div class="impl-card">
                        <div class="impl-title">🔄 Measurement Bases</div>
                        <ul>
                            <li>Computational basis</li>
                            <li>Alternative bases</li>
                            <li>Basis transformation</li>
                            <li>Compatible observables</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <div class="card-title">🔍 Types of Measurements</div>
            <div class="card-content">
                <div class="measurement-grid">
                    <div class="meas-card">
                        <div class="meas-title">📌 Projective Measurements</div>
                        <div class="meas-description">Standard quantum measurements</div>
                        <ul>
                            <li>Von Neumann measurements</li>
                            <li>Complete collapse</li>
                            <li>Orthogonal projectors</li>
                            <li>Repeatable results</li>
                        </ul>
                    </div>
                    <div class="meas-card">
                        <div class="meas-title">🌓 Weak Measurements</div>
                        <div class="meas-description">Partial information extraction</div>
                        <ul>
                            <li>Minimal disturbance</li>
                            <li>Continuous monitoring</li>
                            <li>Quantum trajectories</li>
                            <li>State estimation</li>
                        </ul>
                    </div>
                    <div class="meas-card">
                        <div class="meas-title">🎭 POVM Measurements</div>
                        <div class="meas-description">Generalized measurements</div>
                        <ul>
                            <li>Non-orthogonal states</li>
                            <li>Optimal discrimination</li>
                            <li>Quantum communications</li>
                            <li>State tomography</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <div class="card-title">💡 Measurement Applications</div>
            <div class="card-content">
                <div class="application-grid">
                    <div class="app-card">
                        <div class="app-title">🔐 Quantum Cryptography</div>
                        <div class="app-content">
                            <p>Security Features:</p>
                            <ul>
                                <li>Eavesdropping detection</li>
                                <li>Key distribution</li>
                                <li>State verification</li>
                            </ul>
                        </div>
                    </div>
                    <div class="app-card">
                        <div class="app-title">🔬 Quantum Sensing</div>
                        <div class="app-content">
                            <p>Precision Measurements:</p>
                            <ul>
                                <li>Atomic clocks</li>
                                <li>Magnetic sensors</li>
                                <li>Gravity detection</li>
                            </ul>
                        </div>
                    </div>
                    <div class="app-card">
                        <div class="app-title">💻 Quantum Computing</div>
                        <div class="app-content">
                            <p>Algorithm Outputs:</p>
                            <ul>
                                <li>Result readout</li>
                                <li>Error detection</li>
                                <li>State preparation</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <div class="card-title">🚀 Advanced Techniques</div>
            <div class="card-content">
                <div class="technique-grid">
                    <div class="tech-card">
                        <div class="tech-title">🔄 Quantum State Tomography</div>
                        <ul>
                            <li>Complete state reconstruction</li>
                            <li>Multiple measurement bases</li>
                            <li>Statistical reconstruction</li>
                            <li>Fidelity verification</li>
                        </ul>
                    </div>
                    <div class="tech-card">
                        <div class="tech-title">📊 Error Mitigation</div>
                        <ul>
                            <li>Readout error correction</li>
                            <li>Measurement calibration</li>
                            <li>Noise characterization</li>
                            <li>Post-processing</li>
                        </ul>
                    </div>
                    <div class="tech-card">
                        <div class="tech-title">🎯 Adaptive Measurements</div>
                        <ul>
                            <li>Feedback control</li>
                            <li>Dynamic protocols</li>
                            <li>Optimal strategies</li>
                            <li>Real-time adaptation</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        show_measurements_advanced_content()
        if st.button("Mark as Complete"):
            mark_complete('concepts', 'Quantum Measurements')
            st.success("✅ Topic marked as complete!")
    except Exception as e:
        logger.error(f"Error in show_measurement_content: {str(e)}")
        st.error("An error occurred while displaying measurement content. Please refresh the page.")



def show_concepts():
    """Display quantum computing concepts using tabs"""
    try:
        st.title("Quantum Computing Concepts")

        # Create tabs for different sections
        tabs = st.tabs(["🔄 Qubits", "🎯 Gates", "🔌 Circuits", "📏 Measurements"])

        with tabs[0]:  # Qubits tab
            st.header("Qubits: The Building Blocks of Quantum Computing")
            show_qubit_content()
            st.markdown("### 📝 Test Your Knowledge")
            if st.button("Take Qubit Quiz", key="qubit_quiz"):
                show_quiz("qubits")

        with tabs[1]:  # Gates tab
            st.header("Quantum Gates: Manipulating Quantum Information")
            show_gate_content()
            st.markdown("### 📝 Test Your Knowledge")
            if st.button("Take Gates Quiz", key="gates_quiz"):
                show_quiz("gates")

        with tabs[2]:  # Circuits tab
            st.header("Quantum Circuits: Building Quantum Programs")
            show_circuit_content()
            st.markdown("### 📝 Test Your Knowledge")
            if st.button("Take Circuits Quiz", key="circuits_quiz"):
                show_quiz("circuits")

        with tabs[3]:  # Measurements tab
            st.header("Quantum Measurements: Observing Quantum Systems")
            show_measurement_content()
            st.markdown("### 📝 Test Your Knowledge")
            if st.button("Take Measurements Quiz", key="measurements_quiz"):
                show_quiz("measurements")

    except Exception as e:
        logger.error(f"Error in show_concepts: {str(e)}")
        st.error("An error occurred while displaying concepts. Please refresh the page.")

def show_concept_quiz(concept):
    st.subheader(f"Quiz: {concept}")

    if 'quiz_state' not in st.session_state:
        st.session_state.quiz_state = {}

    quizzes = {
        "Qubits": [
            {
                "question": "What is a qubit?",
                "options": [
                    "A classical bit",
                    "A quantum bit that can be in superposition",
                    "A measurement device",
                    "A type of quantum gate"
                ],
                "correct": 1
            },
            {
                "question": "What is superposition?",
                "options": [
                    "Two qubits in the same state",
                    "A quantum state that is a combination of basis states",
                    "A measurement outcome",
                    "A type of quantum error"
                ],
                "correct": 1
            }
        ],
        "Quantum Gates": [
            {
                "question": "What is the Hadamard gate used for?",
                "options": [
                    "Measuring qubits",
                    "Creating superposition",
                    "Erasing quantum information",
                    "Classical computation"
                ],
                "correct": 1
            },
            {
                "question": "Which gate performs a NOT operation?",
                "options": [
                    "H gate",
                    "Z gate",
                    "X gate",
                    "Y gate"
                ],
                "correct": 2
            }
        ],
        # Add more questions for other concepts
    }

    if concept in quizzes:
        for i, q in enumerate(quizzes[concept]):
            st.write(f"\n**Question {i+1}:** {q['question']}")
            answer = st.radio(
                f"Select your answer for question {i+1}:",
                q['options'],
                key=f"quiz_{concept}_{i}"
            )

            if st.button(f"Check Answer {i+1}", key=f"check_{concept}_{i}"):
                if q['options'].index(answer) == q['correct']:
                    st.success("Correct! 🎉")
                else:
                    st.error("Try again! 🔄")
    else:
        st.info("Quiz content coming soon!")


def show_notes_section(concept):
    st.subheader(f"Notes: {concept}")

    if 'user_notes' not in st.session_state:
        st.session_state.user_notes = {}

    current_notes = st.session_state.user_notes.get(concept, "")

    notes = st.text_area(
        "Write your summary and notes here:",
        value=current_notes,
        height=300,
        key=f"notes_{concept}"
    )

    if st.button("Save Notes"):
        st.session_state.user_notes[concept] = notes
        st.success("Notes saved successfully! 📝")


def generate_pdf_summary(concept):
    st.subheader(f"Download {concept} Summary")

    if st.button("Generate PDF"):
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)

        p.setFont("Helvetica-Bold", 16)
        p.drawString(72, 800, f"Summary: {concept}")

        p.setFont("Helvetica", 12)
        y = 750

        if hasattr(st.session_state, 'user_notes') and concept in st.session_state.user_notes:
            notes = st.session_state.user_notes[concept]
            for line in notes.split('\n'):
                if y > 50:
                    p.drawString(72, y, line)
                    y -= 20

        p.save()

        pdf_bytes = buffer.getvalue()
        b64_pdf = base64.b64encode(pdf_bytes).decode()
        href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="{concept}_summary.pdf">Click here to download your PDF summary</a>'
        st.markdown(href, unsafe_allow_html=True)
        st.success("PDF generated successfully! Click the link above to download.")