import streamlit as st
import random
from collections import defaultdict

# Full chord dictionary with triads, sevenths, and inversions
CHORDS = {
    # Major triads
    "C major root": ["C", "E", "G"],
    "C major 1st inversion": ["E", "G", "C"],
    "C major 2nd inversion": ["G", "C", "E"],
    "C# major root": ["C#", "E#", "G#"],
    "C# major 1st inversion": ["E#", "G#", "C#"],
    "C# major 2nd inversion": ["G#", "C#", "E#"],
    "D major root": ["D", "F#", "A"],
    "D major 1st inversion": ["F#", "A", "D"],
    "D major 2nd inversion": ["A", "D", "F#"],
    "Eb major root": ["Eb", "G", "Bb"],
    "Eb major 1st inversion": ["G", "Bb", "Eb"],
    "Eb major 2nd inversion": ["Bb", "Eb", "G"],
    "E major root": ["E", "G#", "B"],
    "E major 1st inversion": ["G#", "B", "E"],
    "E major 2nd inversion": ["B", "E", "G#"],
    "F major root": ["F", "A", "C"],
    "F major 1st inversion": ["A", "C", "F"],
    "F major 2nd inversion": ["C", "F", "A"],
    "F# major root": ["F#", "A#", "C#"],
    "F# major 1st inversion": ["A#", "C#", "F#"],
    "F# major 2nd inversion": ["C#", "F#", "A#"],
    "G major root": ["G", "B", "D"],
    "G major 1st inversion": ["B", "D", "G"],
    "G major 2nd inversion": ["D", "G", "B"],
    "Ab major root": ["Ab", "C", "Eb"],
    "Ab major 1st inversion": ["C", "Eb", "Ab"],
    "Ab major 2nd inversion": ["Eb", "Ab", "C"],
    "A major root": ["A", "C#", "E"],
    "A major 1st inversion": ["C#", "E", "A"],
    "A major 2nd inversion": ["E", "A", "C#"],
    "Bb major root": ["Bb", "D", "F"],
    "Bb major 1st inversion": ["D", "F", "Bb"],
    "Bb major 2nd inversion": ["F", "Bb", "D"],
    "B major root": ["B", "D#", "F#"],
    "B major 1st inversion": ["D#", "F#", "B"],
    "B major 2nd inversion": ["F#", "B", "D#"],

    # Minor triads
    "C minor root": ["C", "Eb", "G"],
    "C minor 1st inversion": ["Eb", "G", "C"],
    "C minor 2nd inversion": ["G", "C", "Eb"],
    "C# minor root": ["C#", "E", "G#"],
    "C# minor 1st inversion": ["E", "G#", "C#"],
    "C# minor 2nd inversion": ["G#", "C#", "E"],
    "D minor root": ["D", "F", "A"],
    "D minor 1st inversion": ["F", "A", "D"],
    "D minor 2nd inversion": ["A", "D", "F"],
    "Eb minor root": ["Eb", "Gb", "Bb"],
    "Eb minor 1st inversion": ["Gb", "Bb", "Eb"],
    "Eb minor 2nd inversion": ["Bb", "Eb", "Gb"],
    "E minor root": ["E", "G", "B"],
    "E minor 1st inversion": ["G", "B", "E"],
    "E minor 2nd inversion": ["B", "E", "G"],
    "F minor root": ["F", "Ab", "C"],
    "F minor 1st inversion": ["Ab", "C", "F"],
    "F minor 2nd inversion": ["C", "F", "Ab"],
    "F# minor root": ["F#", "A", "C#"],
    "F# minor 1st inversion": ["A", "C#", "F#"],
    "F# minor 2nd inversion": ["C#", "F#", "A"],
    "G minor root": ["G", "Bb", "D"],
    "G minor 1st inversion": ["Bb", "D", "G"],
    "G minor 2nd inversion": ["D", "G", "Bb"],
    "Ab minor root": ["Ab", "Cb", "Eb"],
    "Ab minor 1st inversion": ["Cb", "Eb", "Ab"],
    "Ab minor 2nd inversion": ["Eb", "Ab", "Cb"],
    "A minor root": ["A", "C", "E"],
    "A minor 1st inversion": ["C", "E", "A"],
    "A minor 2nd inversion": ["E", "A", "C"],
    "Bb minor root": ["Bb", "Db", "F"],
    "Bb minor 1st inversion": ["Db", "F", "Bb"],
    "Bb minor 2nd inversion": ["F", "Bb", "Db"],
    "B minor root": ["B", "D", "F#"],
    "B minor 1st inversion": ["D", "F#", "B"],
    "B minor 2nd inversion": ["F#", "B", "D"],

    # Diminished triads
    "C diminished root": ["C", "Eb", "Gb"],
    "C diminished 1st inversion": ["Eb", "Gb", "C"],
    "C diminished 2nd inversion": ["Gb", "C", "Eb"],
    "C# diminished root": ["C#", "E", "G"],
    "C# diminished 1st inversion": ["E", "G", "C#"],
    "C# diminished 2nd inversion": ["G", "C#", "E"],
    "D diminished root": ["D", "F", "Ab"],
    "D diminished 1st inversion": ["F", "Ab", "D"],
    "D diminished 2nd inversion": ["Ab", "D", "F"],
    # ... (add all diminished chords similarly)
}

# Group chords by base name for columns
grouped_chords = defaultdict(list)
for chord_name in CHORDS.keys():
    # The base is first two words (e.g., "C major" or "A minor")
    base = " ".join(chord_name.split()[:2])
    grouped_chords[base].append(chord_name)

base_chords = sorted(grouped_chords.keys())

# Sidebar: select which chords to include
st.sidebar.title("Select Chords for Quiz")
selected_base_chords = st.sidebar.multiselect(
    "Choose base chords:",
    options=base_chords,
    default=["C major", "A minor", "E minor", "G major"]
)

if not selected_base_chords:
    st.warning("Please select at least one chord.")
    st.stop()

# Build selected chords dictionary
selected_chords_dict = {base: grouped_chords[base] for base in selected_base_chords}
all_selected_chords = [ch for sublist in selected_chords_dict.values() for ch in sublist]

# Initialize session state
if "current_chord" not in st.session_state or st.session_state.current_chord not in all_selected_chords:
    st.session_state.current_chord = random.choice(all_selected_chords)
    st.session_state.show_result = False
    st.session_state.result_text = ""

# Next Chord button
if st.button("Next Chord"):
    st.session_state.current_chord = random.choice(all_selected_chords)
    st.session_state.show_result = False
    st.session_state.result_text = ""

# Display current chord notes
chord_key = st.session_state.current_chord
st.write(f"### Notes: {', '.join(CHORDS[chord_key])}")

# Display answer buttons in vertical columns
cols = st.columns(len(selected_base_chords))

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
