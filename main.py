import streamlit as st
from components import circuit_builder, state_visualizer, progress_tracker, auth
from content import quantum_concepts, quantum_algorithms, quantum_hardware
import quantum_utils

def main():
    st.set_page_config(
        page_title="Quantum Computing Education Hub",
        page_icon="⚛️",
        layout="wide"
    )

    # Initialize authentication
    auth.init_auth()

    # Initialize theme
    if 'theme' not in st.session_state:
        st.session_state['theme'] = 'light'

    # Load custom CSS
    with open("assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Load interactive JavaScript
    with open("assets/interactive.js") as f:
        st.markdown(f"<script>{f.read()}</script>", unsafe_allow_html=True)

    # Apply theme
    st.markdown(f"""
        <script>
            function applyTheme(theme) {{
                document.documentElement.setAttribute('data-theme', theme);
                document.body.setAttribute('data-theme', theme);

                const frames = document.getElementsByTagName('iframe');
                for (const frame of frames) {{
                    try {{
                        if (frame.contentDocument) {{
                            frame.contentDocument.documentElement.setAttribute('data-theme', theme);
                            frame.contentDocument.body.setAttribute('data-theme', theme);
                        }}
                    }} catch (e) {{
                        console.log('Could not access iframe');
                    }}
                }}
            }}
            window.addEventListener('load', function() {{
                applyTheme('{st.session_state.theme}');
            }});
        </script>
    """, unsafe_allow_html=True)

    # Show authentication page if not logged in
    if not st.session_state.get('authentication_status'):
        auth.show_auth_page()
        return

    # Initialize progress tracking
    progress_tracker.initialize_progress()

    # Sidebar navigation
    st.sidebar.title("Navigation")

    # Theme toggle in sidebar
    theme = st.sidebar.selectbox(
        "Theme",
        ["Light", "Dark"],
        index=0 if st.session_state.theme == 'light' else 1
    )

    # Update theme in session state and apply immediately
    new_theme = theme.lower()
    if new_theme != st.session_state.theme:
        st.session_state.theme = new_theme
        st.markdown(f"""
            <script>
                applyTheme('{new_theme}');
            </script>
        """, unsafe_allow_html=True)
        st.rerun()

    # Show logout button
    auth.show_logout()

    # Show overall progress
    st.sidebar.subheader("Your Progress")
    concepts_progress = progress_tracker.get_progress('concepts')
    algorithms_progress = progress_tracker.get_progress('algorithms')
    circuit_progress = progress_tracker.get_progress('circuit_builder')

    st.sidebar.write("Quantum Concepts")
    st.sidebar.progress(concepts_progress / 100)

    st.sidebar.write("Circuit Building")
    st.sidebar.progress(circuit_progress / 100)

    st.sidebar.write("Quantum Algorithms")
    st.sidebar.progress(algorithms_progress / 100)

    # Navigation options
    nav_options = ["Home", "Quantum Concepts", "Circuit Builder", "State Visualization", 
                  "Quantum Algorithms", "Quantum Hardware"]

    # Add Admin Panel option for admin users
    if st.session_state.get('is_admin', False):
        nav_options.append("Admin Panel")

    # Navigation
    page = st.sidebar.radio("Select a Topic", nav_options)

    if page == "Home":
        show_home()
    elif page == "Quantum Concepts":
        quantum_concepts.show_concepts()
    elif page == "Circuit Builder":
        circuit_builder.show_circuit_builder()
    elif page == "State Visualization":
        state_visualizer.show_state_visualizer()
    elif page == "Quantum Algorithms":
        quantum_algorithms.show_algorithms()
    elif page == "Quantum Hardware":
        quantum_hardware.show_hardware()
    elif page == "Admin Panel" and st.session_state.get('is_admin', False):
        auth.show_admin_panel()

def show_home():
    st.title(f"Welcome, {st.session_state['username']}!")

    # Introduction section with grid layout
    st.markdown('<div class="section-title">Start Your Quantum Journey</div>', unsafe_allow_html=True)

    # Features grid
    st.markdown('<div class="grid">', unsafe_allow_html=True)

    # Feature cards
    features = [
        {
            "title": "Interactive Learning",
            "description": "Learn quantum computing through hands-on exercises and visualizations.",
            "icon": "🎓"
        },
        {
            "title": "Quantum Circuit Builder",
            "description": "Design and simulate quantum circuits with our intuitive interface.",
            "icon": "⚡"
        },
        {
            "title": "State Visualization",
            "description": "Visualize quantum states and understand quantum mechanics principles.",
            "icon": "🔮"
        },
        {
            "title": "Algorithm Explorer",
            "description": "Discover and experiment with quantum algorithms.",
            "icon": "🧮"
        },
        {
            "title": "Hardware Deep Dive",
            "description": "Learn about quantum computing hardware implementations.",
            "icon": "🔧"
        },
        {
            "title": "Progress Tracking",
            "description": "Track your learning progress and achievements.",
            "icon": "📊"
        }
    ]

    for feature in features:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">{feature['icon']} {feature['title']}</div>
            <div class="card-content">{feature['description']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Progress section
    st.markdown('<div class="section-title">Your Learning Progress</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Quantum Concepts")
        progress_tracker.show_progress_bar('concepts')
        next_topic = progress_tracker.get_next_topic('concepts')
        if next_topic:
            st.info(f"Next topic: {next_topic}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Circuit Building")
        progress_tracker.show_progress_bar('circuit_builder')
        next_topic = progress_tracker.get_next_topic('circuit_builder')
        if next_topic:
            st.info(f"Next topic: {next_topic}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Quantum Algorithms")
        progress_tracker.show_progress_bar('algorithms')
        next_topic = progress_tracker.get_next_topic('algorithms')
        if next_topic:
            st.info(f"Next topic: {next_topic}")
        st.markdown('</div>', unsafe_allow_html=True)

    # Quick start section
    st.markdown('<div class="section-title">Quick Start</div>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    if st.button("Run Sample Quantum Circuit", key="quick_start"):
        result = quantum_utils.run_sample_circuit()
        st.write("Sample circuit result:", result)
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()