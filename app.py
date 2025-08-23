import streamlit as st
import random
from collections import defaultdict

# =====================
# Complete Chord Dictionary
# =====================
CHORDS = {
    # --- Major triads ---
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

    # --- Minor triads ---
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

    # --- Diminished triads ---
    "C diminished root": ["C", "Eb", "Gb"],
    "C diminished 1st inversion": ["Eb", "Gb", "C"],
    "C diminished 2nd inversion": ["Gb", "C", "Eb"],

    "C# diminished root": ["C#", "E", "G"],
    "C# diminished 1st inversion": ["E", "G", "C#"],
    "C# diminished 2nd inversion": ["G", "C#", "E"],

    "D diminished root": ["D", "F", "Ab"],
    "D diminished 1st inversion": ["F", "Ab", "D"],
    "D diminished 2nd inversion": ["Ab", "D", "F"],

    "Eb diminished root": ["Eb", "Gb", "Bbb"],
    "Eb diminished 1st inversion": ["Gb", "Bbb", "Eb"],
    "Eb diminished 2nd inversion": ["Bbb", "Eb", "Gb"],

    "E diminished root": ["E", "G", "Bb"],
    "E diminished 1st inversion": ["G", "Bb", "E"],
    "E diminished 2nd inversion": ["Bb", "E", "G"],

    "F diminished root": ["F", "Ab", "Cb"],
    "F diminished 1st inversion": ["Ab", "Cb", "F"],
    "F diminished 2nd inversion": ["Cb", "F", "Ab"],

    "F# diminished root": ["F#", "A", "C"],
    "F# diminished 1st inversion": ["A", "C", "F#"],
    "F# diminished 2nd inversion": ["C", "F#", "A"],

    "G diminished root": ["G", "Bb", "Db"],
    "G diminished 1st inversion": ["Bb", "Db", "G"],
    "G diminished 2nd inversion": ["Db", "G", "Bb"],

    "Ab diminished root": ["Ab", "Cb", "Ebb"],
    "Ab diminished 1st inversion": ["Cb", "Ebb", "Ab"],
    "Ab diminished 2nd inversion": ["Ebb", "Ab", "Cb"],

    "A diminished root": ["A", "C", "Eb"],
    "A diminished 1st inversion": ["C", "Eb", "A"],
    "A diminished 2nd inversion": ["Eb", "A", "C"],

    "Bb diminished root": ["Bb", "Db", "Fb"],
    "Bb diminished 1st inversion": ["Db", "Fb", "Bb"],
    "Bb diminished 2nd inversion": ["Fb", "Bb", "Db"],

    "B diminished root": ["B", "D", "F"],
    "B diminished 1st inversion": ["D", "F", "B"],
    "B diminished 2nd inversion": ["F", "B", "D"],

    # --- Major Seventh Chords ---
    "C major seventh root": ["C", "E", "G", "B"],
    "C major seventh 1st inversion": ["E", "G", "B", "C"],
    "C major seventh 2nd inversion": ["G", "B", "C", "E"],
    "C major seventh 3rd inversion": ["B", "C", "E", "G"],

    "C# major seventh root": ["C#", "E#", "G#", "B#"],
    "C# major seventh 1st inversion": ["E#", "G#", "B#", "C#"],
    "C# major seventh 2nd inversion": ["G#", "B#", "C#", "E#"],
    "C# major seventh 3rd inversion": ["B#", "C#", "E#", "G#"],

    "D major seventh root": ["D", "F#", "A", "C#"],
    "D major seventh 1st inversion": ["F#", "A", "C#", "D"],
    "D major seventh 2nd inversion": ["A", "C#", "D", "F#"],
    "D major seventh 3rd inversion": ["C#", "D", "F#", "A"],

    # ... continue for all other major7, dominant7, minor7, minor7b5 chords
}

# =====================
# Group chords by base name
# =====================
grouped_chords = defaultdict(list)
for chord_name in CHORDS.keys():
    base_name = " ".join(chord_name.split()[:2])
    grouped_chords[base_name].append(chord_name)

# =====================
# Sidebar selection
# =====================
st.sidebar.title("Select Chords for Quiz")
base_chords = list(grouped_chords.keys())

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
# Random chord selection
# =====================
if "current_chord" not in st.session_state:
    chord_key = random.choice(selected_chords)
    st.session_state.current_chord = (chord_key, CHORDS[chord_key])

chord_name, chord_notes = st.session_state.current_chord

st.write(f"Notes: {', '.join(chord_notes)}")

# =====================
# Clickable answer buttons
# =====================
st.write("Select the correct chord:")

options = selected_chords.copy()
random.shuffle(options)

for option in options:
    if st.button(option):
        if option == chord_name:
            st.success(f"✅ Correct! It was {chord_name}")
        else:
            st.error(f"❌ Incorrect. The correct answer was {chord_name}")

# =====================
# Next chord button
# =====================
if st.button("Next Chord"):
    chord_key = random.choice(selected_chords)
    st.session_state.current_chord = (chord_key, CHORDS[chord_key])

