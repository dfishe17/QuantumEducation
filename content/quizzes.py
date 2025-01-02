import streamlit as st
import random
from typing import List, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QuizQuestion:
    def __init__(self, question: str, choices: List[str], correct_answer: int, 
                 explanation: str, difficulty: str):
        self.question = question
        self.choices = choices
        self.correct_answer = correct_answer
        self.explanation = explanation
        self.difficulty = difficulty

# Qubit Quiz Questions
qubit_questions = [
    QuizQuestion(
        "What is a qubit?",
        [
            "A classical bit that can only be 0 or 1",
            "A quantum system that can exist in a superposition of states",
            "A measurement device for quantum computers",
            "A type of quantum error correction"
        ],
        1,
        "A qubit is the fundamental unit of quantum information that can exist in a superposition of states, unlike classical bits which can only be 0 or 1.",
        "Easy"
    ),
    QuizQuestion(
        "What is quantum superposition?",
        [
            "When two qubits are entangled",
            "When a qubit is measured",
            "When a qubit exists in multiple states simultaneously",
            "When a qubit is initialized to |0⟩"
        ],
        2,
        "Superposition allows a qubit to exist in multiple states simultaneously until measured, a key feature of quantum computing.",
        "Easy"
    ),
    QuizQuestion(
        "What does the Bloch sphere represent?",
        [
            "The space of all possible classical bit states",
            "The physical structure of a quantum computer",
            "The geometric representation of a single qubit state",
            "The visualization of quantum entanglement"
        ],
        2,
        "The Bloch sphere is a geometric representation of the pure state space of a single qubit.",
        "Medium"
    ),
    QuizQuestion(
        "What is quantum entanglement?",
        [
            "A type of quantum error",
            "When qubits are perfectly isolated",
            "A correlation between quantum states that can't be described classically",
            "The process of measuring a qubit"
        ],
        2,
        "Entanglement is a quantum phenomenon where two or more particles become correlated in a way that can't be explained by classical physics.",
        "Medium"
    ),
    QuizQuestion(
        "Which property is NOT preserved in quantum measurement?",
        [
            "Energy",
            "Superposition",
            "Spin",
            "Angular momentum"
        ],
        1,
        "Measurement collapses the quantum superposition, making it one of the fundamental challenges in quantum computing.",
        "Hard"
    ),
    QuizQuestion(
        "What is the mathematical condition for a valid qubit state |ψ⟩ = α|0⟩ + β|1⟩?",
        [
            "|α|² + |β|² = 0",
            "|α|² + |β|² = 1",
            "|α|² + |β|² = 2",
            "α + β = 1"
        ],
        1,
        "The normalization condition |α|² + |β|² = 1 ensures the total probability of measuring the qubit is 1.",
        "Hard"
    ),
    QuizQuestion(
        "What is decoherence in quantum computing?",
        [
            "The process of initializing qubits",
            "The loss of quantum information due to environment interaction",
            "A type of quantum gate operation",
            "The measurement of quantum states"
        ],
        1,
        "Decoherence is the loss of quantum information due to unwanted interactions with the environment.",
        "Medium"
    ),
    QuizQuestion(
        "Which is NOT a common physical implementation of qubits?",
        [
            "Superconducting circuits",
            "Trapped ions",
            "Classical transistors",
            "Quantum dots"
        ],
        2,
        "Classical transistors operate based on classical physics and cannot maintain quantum superposition.",
        "Medium"
    ),
    QuizQuestion(
        "What is the no-cloning theorem?",
        [
            "A theorem about quantum error correction",
            "A theorem stating quantum states cannot be perfectly copied",
            "A theorem about quantum teleportation",
            "A theorem about quantum measurement"
        ],
        1,
        "The no-cloning theorem states that it's impossible to create an exact copy of an arbitrary unknown quantum state.",
        "Hard"
    ),
    QuizQuestion(
        "What is the main advantage of using qubits over classical bits?",
        [
            "They're easier to manufacture",
            "They can store exponentially more information",
            "They're more stable",
            "They operate at room temperature"
        ],
        1,
        "Qubits can exist in superposition and become entangled, allowing quantum computers to process exponentially more information than classical computers.",
        "Easy"
    ),
    QuizQuestion(
        "What is quantum tunneling?",
        [
            "A classical phenomenon in electrical circuits",
            "A quantum effect where particles pass through energy barriers",
            "A type of quantum gate operation",
            "A method for measuring qubits"
        ],
        1,
        "Quantum tunneling is a quantum mechanical phenomenon where particles can pass through potential energy barriers that they classically couldn't overcome.",
        "Hard"
    ),
    QuizQuestion(
        "What is a quantum register?",
        [
            "A classical memory storage device",
            "A collection of qubits that can be manipulated together",
            "A type of quantum measurement device",
            "A quantum error correction code"
        ],
        1,
        "A quantum register is a collection of qubits that can be manipulated together to perform quantum computations.",
        "Medium"
    ),
    QuizQuestion(
        "What is the difference between mixed and pure quantum states?",
        [
            "Pure states are always measured as |0⟩, mixed states as |1⟩",
            "Mixed states are easier to maintain than pure states",
            "Pure states can be described by a single state vector, mixed states are statistical mixtures",
            "There is no difference between them"
        ],
        2,
        "Pure states are quantum states that can be described by a single state vector, while mixed states represent statistical mixtures of pure states.",
        "Hard"
    )
]

# Quantum Gates Quiz Questions
gate_questions = [
    QuizQuestion(
        "What is a quantum gate?",
        [
            "A physical barrier in quantum computers",
            "A unitary operation that manipulates quantum states",
            "A measurement device",
            "A type of quantum error"
        ],
        1,
        "Quantum gates are unitary operations that manipulate quantum states, similar to classical logic gates but preserving quantum properties.",
        "Easy"
    ),
    QuizQuestion(
        "What does the Hadamard gate do?",
        [
            "Measures a qubit",
            "Creates entanglement",
            "Creates an equal superposition from basis states",
            "Performs a NOT operation"
        ],
        2,
        "The Hadamard gate creates an equal superposition of |0⟩ and |1⟩ states, essential for many quantum algorithms.",
        "Medium"
    ),
    QuizQuestion(
        "Which gate performs a NOT operation on a qubit?",
        [
            "Z gate",
            "H gate",
            "X gate",
            "T gate"
        ],
        2,
        "The X gate (Pauli-X) performs the quantum equivalent of a classical NOT operation.",
        "Easy"
    ),
    QuizQuestion(
        "What is the CNOT gate?",
        [
            "A single-qubit gate",
            "A three-qubit gate",
            "A two-qubit controlled operation",
            "A measurement operation"
        ],
        2,
        "The CNOT (Controlled-NOT) gate is a two-qubit gate where one qubit controls whether to apply an X gate to the target qubit.",
        "Medium"
    ),
    QuizQuestion(
        "Which property must all quantum gates satisfy?",
        [
            "Commutativity",
            "Unitarity",
            "Associativity",
            "Distributivity"
        ],
        1,
        "Quantum gates must be unitary to preserve quantum information and ensure reversibility.",
        "Hard"
    ),
    QuizQuestion(
        "What is the Toffoli gate?",
        [
            "A single-qubit gate",
            "A two-qubit gate",
            "A three-qubit controlled operation",
            "A measurement gate"
        ],
        2,
        "The Toffoli (CCNOT) gate is a three-qubit gate where two control qubits determine whether to apply an X gate to the target.",
        "Medium"
    ),
    QuizQuestion(
        "Which gate adds a π/4 phase?",
        [
            "S gate",
            "T gate",
            "Z gate",
            "H gate"
        ],
        1,
        "The T gate adds a π/4 phase, important for universal quantum computation.",
        "Hard"
    ),
    QuizQuestion(
        "What is the main purpose of controlled gates?",
        [
            "To measure qubits",
            "To create entanglement",
            "To perform error correction",
            "To initialize qubits"
        ],
        1,
        "Controlled gates are essential for creating entanglement between qubits and implementing quantum algorithms.",
        "Medium"
    ),
    QuizQuestion(
        "Which is NOT a common single-qubit gate?",
        [
            "X gate",
            "Y gate",
            "SWAP gate",
            "Z gate"
        ],
        2,
        "The SWAP gate is a two-qubit gate that exchanges the states of two qubits.",
        "Medium"
    ),
    QuizQuestion(
        "What is gate fidelity?",
        [
            "The speed of gate operations",
            "The accuracy of gate implementation",
            "The number of qubits in a gate",
            "The gate's energy consumption"
        ],
        1,
        "Gate fidelity measures how accurately a quantum gate operation is implemented compared to its ideal behavior.",
        "Hard"
    ),
    QuizQuestion(
        "What is quantum gate decomposition?",
        [
            "Breaking a quantum circuit into simpler gates",
            "Measuring the output of quantum gates",
            "A type of quantum error",
            "The physical construction of quantum gates"
        ],
        0,
        "Gate decomposition is the process of breaking down complex quantum operations into sequences of simpler, implementable gates.",
        "Hard"
    ),
    QuizQuestion(
        "What is the phase kickback effect?",
        [
            "A type of quantum error",
            "When a control qubit gains phase from a target qubit",
            "The decoherence of quantum gates",
            "A measurement technique"
        ],
        1,
        "Phase kickback is a quantum effect where a control qubit acquires a phase change based on operations performed on a target qubit.",
        "Hard"
    ),
    QuizQuestion(
        "Which quantum gate is its own inverse?",
        [
            "T gate",
            "S gate",
            "Hadamard gate",
            "Phase gate"
        ],
        2,
        "The Hadamard gate is self-inverse, meaning H² = I (identity). Applying it twice returns the qubit to its original state.",
        "Medium"
    )
]

# New Circuit Questions
circuit_questions = [
    QuizQuestion(
        "What is a quantum circuit?",
        [
            "A classical electronic circuit",
            "A sequence of quantum gates and measurements",
            "A type of quantum computer",
            "A quantum error correction code"
        ],
        1,
        "A quantum circuit is a sequence of quantum gates, measurements, and other operations applied to qubits to perform quantum computations.",
        "Easy"
    ),
    QuizQuestion(
        "What is circuit depth?",
        [
            "The physical size of a quantum circuit",
            "The number of qubits in a circuit",
            "The longest path from input to output in terms of gate operations",
            "The total number of gates in a circuit"
        ],
        2,
        "Circuit depth is the length of the longest path from input to output in a quantum circuit, measured in terms of sequential gate operations.",
        "Medium"
    ),
    QuizQuestion(
        "What is quantum circuit optimization?",
        [
            "Making circuits physically smaller",
            "Reducing the number of qubits",
            "Reducing circuit depth and gate count while preserving functionality",
            "Increasing the circuit's speed"
        ],
        2,
        "Circuit optimization involves reducing the depth and gate count of a quantum circuit while maintaining its intended functionality.",
        "Medium"
    )
]

# New Measurement Questions
measurement_questions = [
    QuizQuestion(
        "What is quantum measurement?",
        [
            "A way to copy quantum states",
            "The process of observing a quantum system, causing wavefunction collapse",
            "A type of quantum gate",
            "A method of quantum error correction"
        ],
        1,
        "Quantum measurement is the process of observing a quantum system, which causes the wavefunction to collapse into a definite state.",
        "Easy"
    ),
    QuizQuestion(
        "What is the quantum Zeno effect?",
        [
            "A type of quantum gate",
            "The process of quantum teleportation",
            "Frequent measurements preventing quantum state evolution",
            "A form of quantum error correction"
        ],
        2,
        "The quantum Zeno effect is a phenomenon where frequent measurements can prevent a quantum system from evolving.",
        "Hard"
    ),
    QuizQuestion(
        "What is a POVM measurement?",
        [
            "A type of quantum gate",
            "A generalized measurement framework in quantum mechanics",
            "A classical measurement technique",
            "A quantum error correction protocol"
        ],
        1,
        "POVM (Positive Operator-Valued Measure) is a generalized framework for describing quantum measurements beyond projective measurements.",
        "Hard"
    )
]

def show_quiz(topic: str):
    """Display a quiz for the specified topic"""
    try:
        logger.info(f"Starting quiz for topic: {topic}")

        # Select questions based on topic
        if topic.lower() == "qubits":
            questions = qubit_questions
        elif topic.lower() == "gates":
            questions = gate_questions
        elif topic.lower() == "circuits":
            questions = circuit_questions
        elif topic.lower() == "measurements":
            questions = measurement_questions
        else:
            logger.error(f"Unknown quiz topic: {topic}")
            st.error(f"Quiz for {topic} is not available.")
            return

        st.header(f"{topic.title()} Quiz")

        if "quiz_score" not in st.session_state:
            st.session_state.quiz_score = 0
        if "questions_answered" not in st.session_state:
            st.session_state.questions_answered = 0

        # Display one question at a time
        if st.session_state.questions_answered < len(questions):
            current_question = questions[st.session_state.questions_answered]

            # Display question difficulty
            st.markdown(f"**Difficulty:** {current_question.difficulty}")

            # Display question
            st.markdown(f"**Question {st.session_state.questions_answered + 1}:** {current_question.question}")

            # Display choices
            answer = st.radio("Select your answer:", 
                            current_question.choices,
                            key=f"quiz_{st.session_state.questions_answered}")

            if st.button("Submit Answer"):
                if answer == current_question.choices[current_question.correct_answer]:
                    st.success("Correct! 🎉")
                    st.session_state.quiz_score += 1
                else:
                    st.error("Incorrect.")

                # Show explanation
                st.info(f"Explanation: {current_question.explanation}")

                st.session_state.questions_answered += 1

                # Show progress
                if st.session_state.questions_answered < len(questions):
                    st.button("Next Question")

        # Show final score
        if st.session_state.questions_answered == len(questions):
            score_percentage = (st.session_state.quiz_score / len(questions)) * 100
            st.success(f"Quiz completed! Your score: {st.session_state.quiz_score}/{len(questions)} ({score_percentage:.1f}%)")

            # Provide feedback based on score
            if score_percentage >= 90:
                st.markdown("🌟 Excellent! You have a strong understanding of the topic!")
            elif score_percentage >= 70:
                st.markdown("👍 Good job! Keep practicing to improve further.")
            else:
                st.markdown("📚 Consider reviewing the material and trying again.")

            # Reset button
            if st.button("Retake Quiz"):
                st.session_state.quiz_score = 0
                st.session_state.questions_answered = 0
                st.rerun()

        # Show progress bar
        progress = st.session_state.questions_answered / len(questions)
        st.progress(progress)

    except Exception as e:
        logger.error(f"Error in show_quiz: {str(e)}")
        st.error("An error occurred while displaying the quiz. Please try again.")

def get_quiz_topics() -> List[str]:
    """Return available quiz topics"""
    return ["Qubits", "Gates", "Circuits", "Measurements"]