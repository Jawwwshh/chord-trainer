import streamlit as st
import random
from collections import defaultdict

# =====================
# Full Chord Dictionary (example subset)
# You would expand this with all chords and inversions as before
# =====================
CHORDS = {
    # Major triads (example)
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

    # Add all other chords from your full list here...
}

# =====================
# Group chords by base name
# =====================
grouped_chords = defaultdict(list)
for chord_name in CHORDS.keys():
    name_lower = chord_name.lower()
    if "seventh" in name_lower:
        base_name = " ".join(chord_name.split()[:3])
    else:
        base_name = " ".join(chord_name.split()[:2])
    grouped_chords[base_name].append(chord_name)

# Alphabetical list of base chords for sidebar
base_chords = sorted(grouped_chords.keys())

# =====================
# Sidebar: select base chords
# =====================
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

# Default to all chords if nothing selected
if not selected_chords:
    selected_chords = list(CHORDS.keys())

# =====================
# Initialize current chord if not set
# =====================
if "current_chord" not in st.session_state:
    st.session_state.current_chord = random.choice(selected_chords)
    st.session_state.show_result = False
    st.session_state.result = None

chord_key = st.session_state.current_chord
chord_notes = CHORDS[chord_key]

# =====================
# Display the notes
# =====================
st.write(f"### Notes: {', '.join(chord_notes)}")

# =====================
# Answer buttons in horizontal layout
# =====================
st.write("### Select the correct chord:")

# Sort selected chords alphabetically
sorted_options = sorted(selected_chords)

# Determine number of columns for horizontal layout
num_cols = min(4, len(sorted_options))  # you can adjust number of columns
columns = st.columns(num_cols)

for idx, option in enumerate(sorted_options):
    col = columns[idx % num_cols]
    if col.button(option):
        if option == chord_key:
            st.session_state.result = f"✅ Correct! It was {chord_key}"
        else:
            st.session_state.result = f"❌ Incorrect. The correct answer was {chord_key}"
        st.session_state.show_result = True

# Show result
if st.session_state.show_result and st.session_state.result:
    st.write(st.session_state.result)

# =====================
# Next chord button
# =====================
if st.button("Next Chord"):
    st.session_state.current_chord = random.choice(selected_chords)
    st.session_state.show_result = False
    st.session_state.result = None

