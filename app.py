import streamlit as st
import random
from collections import defaultdict

# Example chord dictionary
CHORDS = {
    "C major root": ["C", "E", "G"],
    "C major 1st inversion": ["E", "G", "C"],
    "C major 2nd inversion": ["G", "C", "E"],
    "A minor root": ["A", "C", "E"],
    "A minor 1st inversion": ["C", "E", "A"],
    "A minor 2nd inversion": ["E", "A", "C"],
}

# Group chords by base name
grouped_chords = defaultdict(list)
for chord_name in CHORDS.keys():
    base = " ".join(chord_name.split()[:2])
    grouped_chords[base].append(chord_name)

base_chords = sorted(grouped_chords.keys())

# Sidebar selection
st.sidebar.title("Select Chords for Quiz")
selected_base_chords = st.sidebar.multiselect(
    "Choose base chords:",
    options=base_chords,
    default=["C major"]
)

if not selected_base_chords:
    st.warning("Please select at least one chord.")
    st.stop()

# Selected chords dictionary
selected_chords_dict = {base: grouped_chords[base] for base in selected_base_chords}
all_selected_chords = [ch for sublist in selected_chords_dict.values() for ch in sublist]

# Initialize current chord
if "current_chord" not in st.session_state or st.session_state.current_chord not in all_selected_chords:
    st.session_state.current_chord = random.choice(all_selected_chords)
    st.session_state.show_result = False
    st.session_state.result_text = ""

# Next Chord button
if st.button("Next Chord"):
    st.session_state.current_chord = random.choice(all_selected_chords)
    st.session_state.show_result = False
    st.session_state.result_text = ""

# Display notes
chord_key = st.session_state.current_chord
st.write(f"### Notes: {', '.join(CHORDS[chord_key])}")

# Make at least 1 column
num_cols = max(len(selected_base_chords), 1)
cols = st.columns(num_cols)

# Display buttons vertically in columns
for col_idx, base in enumerate(selected_base_chords):
    with cols[col_idx]:
        st.write(f"**{base}**")
        for option in selected_chords_dict[base]:
            if st.button(option, key=f"{option}"):
                if option == chord_key:
                    st.session_state.result_text = f"✅ Correct! It was {chord_key}"
                else:
                    st.session_state.result_text = f"❌ Incorrect. The correct answer was {chord_key}"
                st.session_state.show_result = True

# Show result
if st.session_state.show_result:
    st.write(st.session_state.result_text)
