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

# Sidebar: select which chords to include
st.sidebar.title("Select Chords for Quiz")
selected_base_chords = st.sidebar.multiselect(
    "Choose base chords to include:",
    options=base_chords,
    default=["A minor", "C major", "E minor", "G major"]
)

# Build selected chords dictionary for columns
selected_chords_dict = {base: grouped_chords[base] for base in selected_base_chords}

# Flattened list of all selected chords
all_selected_chords = [ch for sublist in selected_chords_dict.values() for ch in sublist]

# Initialize session state
if "current_chord" not in st.session_state:
    st.session_state.current_chord = random.choice(all_selected_chords)
    st.session_state.show_result = False
    st.session_state.result_text = ""

# --- NEW FIX: if current_chord is no longer in selected chords, pick a new one ---
if st.session_state.current_chord not in all_selected_chords:
    st.session_state.current_chord = random.choice(all_selected_chords)
    st.session_state.show_result = False
    st.session_state.result_text = ""

# Handle Next Chord
if st.button("Next Chord"):
    st.session_state.current_chord = random.choice(all_selected_chords)
    st.session_state.show_result = False

