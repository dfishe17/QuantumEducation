import streamlit as st

def initialize_progress():
    """Initialize progress tracking in session state if not already present."""
    if 'user_progress' not in st.session_state:
        st.session_state.user_progress = {
            'concepts': {
                'Qubits': False,
                'Quantum Gates': False,
                'Quantum Circuits': False,
                'Quantum Measurements': False
            },
            'circuit_builder': {
                'basic_circuit': False,
                'multi_qubit': False
            },
            'algorithms': {
                'Deutsch': False,
                'Grover': False,
                'QFT': False
            }
        }

def mark_complete(section, topic):
    """Mark a specific topic as completed."""
    if section in st.session_state.user_progress:
        if topic in st.session_state.user_progress[section]:
            st.session_state.user_progress[section][topic] = True

def get_progress(section):
    """Get completion percentage for a section."""
    if section in st.session_state.user_progress:
        completed = sum(st.session_state.user_progress[section].values())
        total = len(st.session_state.user_progress[section])
        return (completed / total) * 100 if total > 0 else 0
    return 0

def show_progress_bar(section):
    """Display a progress bar for the given section."""
    progress = get_progress(section)
    st.progress(progress / 100)
    st.write(f"Progress: {progress:.1f}%")

def is_topic_completed(section, topic):
    """Check if a specific topic is completed."""
    return st.session_state.user_progress.get(section, {}).get(topic, False)

def get_next_topic(section):
    """Get the next uncompleted topic in a section."""
    for topic, completed in st.session_state.user_progress.get(section, {}).items():
        if not completed:
            return topic
    return None
