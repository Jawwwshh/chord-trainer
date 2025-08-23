import streamlit as st
import random
from collections import defaultdict

# Example chords subset
CHORDS = {
    "C major root": ["C", "E", "G"],
    "C major 1st inversion": ["E", "G", "C"],
    "C major 2nd inversion": ["G", "C", "E"],
    "A minor root": ["A", "C", "E"],
    "A minor 1st inversion": ["C", "E", "A"],
    "A minor 2nd inversion": ["E", "A", "C"],
    "G major root": ["G", "B", "D"],
    "G major 1st inversion": ["B", "D", "G"],
    "G major 2nd inversion": ["D", "G", "B"],
    "E minor root": ["E", "G", "B"],
    "E minor 1st inversion": ["G", "B", "E"],
    "E minor 2nd inversion": ["B", "E", "G"],
}

# Group chords by base name
grouped_chords = defaultdict(list)
for chord_name in CHORDS.keys():
    if "seventh" in chord_name.lower():
        base = " ".join(chord_name.split()[:3])
    else:
        base = " ".join(chord_name.split()[:2])
    grouped_chords[base].append(chord_name)

base_chords = sorted(grouped_chords.keys())

# Sidebar chord selection
st.sidebar.title("Select Chords for Quiz")
selected_base_chords = st.sidebar.multiselect(
    "Choose base chords to include:",
    options=base_chords,
    default=["C major", "A minor", "G major", "E minor"]
)

# Build list of all selected chords including inversions
selected_chords = []
for base in selected_base_chords:
    selected_chords.extend(grouped_chords[base])
if not selected_chords:
    selected_chords = list(CHORDS.keys())

# Initialize session state
if "current_chord" not in st.session_state:
    st.session_state.current_chord = random.choice(selected_chords)
    st.session_state.options = sorted(selected_chords)
    st.session_state.show_result = False
    st.session_state.result_text = ""

# Handle Next Chord
if st.button("Next Chord"):
    st.session_state.current_chord = random.choice(selected_chords)
    st.session_state.show_result = False
    st.session_state.result_text = ""

# Display current chord notes
chord_key = st.session_state.current_chord
st.write(f"### Notes: {', '.join(CHORDS[chord_key])}")

# Display answer buttons in columns
cols = st.columns(min(4, len(selected_chords)))  # adjust number of columns
for idx, option in enumerate(st.session_state.options):
    col = cols[idx % len(cols)]
    if col.button(option):
        if option == chord_key:
            st.session_state.result_text = f"✅ Correct! It was {chord_key}"
        else:
            st.session_state.result_text = f"❌ Incorrect. The correct answer was {chord_key}"
        st.session_state.show_result = True

# Show result
if st.session_state.show_result:
    st.write(st.session_state.result_text)

