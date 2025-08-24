import streamlit as st
import random
from collections import defaultdict
from PIL import Image, ImageDraw

# --- MODE SELECTION (top of page) ---
mode = st.sidebar.selectbox("Select Mode", ["identify the position", "Playing the Position"])

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

    # Major sevenths
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
    "Eb major seventh root": ["Eb", "G", "Bb", "D"],
    "Eb major seventh 1st inversion": ["G", "Bb", "D", "Eb"],
    "Eb major seventh 2nd inversion": ["Bb", "D", "Eb", "G"],
    "Eb major seventh 3rd inversion": ["D", "Eb", "G", "Bb"],
    "E major seventh root": ["E", "G#", "B", "D#"],
    "E major seventh 1st inversion": ["G#", "B", "D#", "E"],
    "E major seventh 2nd inversion": ["B", "D#", "E", "G#"],
    "E major seventh 3rd inversion": ["D#", "E", "G#", "B"],
    "F major seventh root": ["F", "A", "C", "E"],
    "F major seventh 1st inversion": ["A", "C", "E", "F"],
    "F major seventh 2nd inversion": ["C", "E", "F", "A"],
    "F major seventh 3rd inversion": ["E", "F", "A", "C"],
    "F# major seventh root": ["F#", "A#", "C#", "E#"],
    "F# major seventh 1st inversion": ["A#", "C#", "E#", "F#"],
    "F# major seventh 2nd inversion": ["C#", "E#", "F#", "A#"],
    "F# major seventh 3rd inversion": ["E#", "F#", "A#", "C#"],
    "G major seventh root": ["G", "B", "D", "F#"],
    "G major seventh 1st inversion": ["B", "D", "F#", "G"],
    "G major seventh 2nd inversion": ["D", "F#", "G", "B"],
    "G major seventh 3rd inversion": ["F#", "G", "B", "D"],
    "Ab major seventh root": ["Ab", "C", "Eb", "G"],
    "Ab major seventh 1st inversion": ["C", "Eb", "G", "Ab"],
    "Ab major seventh 2nd inversion": ["Eb", "G", "Ab", "C"],
    "Ab major seventh 3rd inversion": ["G", "Ab", "C", "Eb"],
    "A major seventh root": ["A", "C#", "E", "G#"],
    "A major seventh 1st inversion": ["C#", "E", "G#", "A"],
    "A major seventh 2nd inversion": ["E", "G#", "A", "C#"],
    "A major seventh 3rd inversion": ["G#", "A", "C#", "E"],
    "Bb major seventh root": ["Bb", "D", "F", "A"],
    "Bb major seventh 1st inversion": ["D", "F", "A", "Bb"],
    "Bb major seventh 2nd inversion": ["F", "A", "Bb", "D"],
    "Bb major seventh 3rd inversion": ["A", "Bb", "D", "F"],
    "B major seventh root": ["B", "D#", "F#", "A#"],
    "B major seventh 1st inversion": ["D#", "F#", "A#", "B"],
    "B major seventh 2nd inversion": ["F#", "A#", "B", "D#"],
    "B major seventh 3rd inversion": ["A#", "B", "D#", "F#"],

    # Dominant sevenths
    "C dominant seventh root": ["C", "E", "G", "Bb"],
    "C dominant seventh 1st inversion": ["E", "G", "Bb", "C"],
    "C dominant seventh 2nd inversion": ["G", "Bb", "C", "E"],
    "C dominant seventh 3rd inversion": ["Bb", "C", "E", "G"],
    "C# dominant seventh root": ["C#", "E#", "G#", "B"],
    "C# dominant seventh 1st inversion": ["E#", "G#", "B", "C#"],
    "C# dominant seventh 2nd inversion": ["G#", "B", "C#", "E#"],
    "C# dominant seventh 3rd inversion": ["B", "C#", "E#", "G#"],
    "D dominant seventh root": ["D", "F#", "A", "C"],
    "D dominant seventh 1st inversion": ["F#", "A", "C", "D"],
    "D dominant seventh 2nd inversion": ["A", "C", "D", "F#"],
    "D dominant seventh 3rd inversion": ["C", "D", "F#", "A"],
    "Eb dominant seventh root": ["Eb", "G", "Bb", "Db"],
    "Eb dominant seventh 1st inversion": ["G", "Bb", "Db", "Eb"],
    "Eb dominant seventh 2nd inversion": ["Bb", "Db", "Eb", "G"],
    "Eb dominant seventh 3rd inversion": ["Db", "Eb", "G", "Bb"],
    "E dominant seventh root": ["E", "G#", "B", "D"],
    "E dominant seventh 1st inversion": ["G#", "B", "D", "E"],
    "E dominant seventh 2nd inversion": ["B", "D", "E", "G#"],
    "E dominant seventh 3rd inversion": ["D", "E", "G#", "B"],
    "F dominant seventh root": ["F", "A", "C", "Eb"],
    "F dominant seventh 1st inversion": ["A", "C", "Eb", "F"],
    "F dominant seventh 2nd inversion": ["C", "Eb", "F", "A"],
    "F dominant seventh 3rd inversion": ["Eb", "F", "A", "C"],
    "F# dominant seventh root": ["F#", "A#", "C#", "E"],
    "F# dominant seventh 1st inversion": ["A#", "C#", "E", "F#"],
    "F# dominant seventh 2nd inversion": ["C#", "E", "F#", "A#"],
    "F# dominant seventh 3rd inversion": ["E", "F#", "A#", "C#"],
    "G dominant seventh root": ["G", "B", "D", "F"],
    "G dominant seventh 1st inversion": ["B", "D", "F", "G"],
    "G dominant seventh 2nd inversion": ["D", "F", "G", "B"],
    "G dominant seventh 3rd inversion": ["F", "G", "B", "D"],
    "Ab dominant seventh root": ["Ab", "C", "Eb", "Gb"],
    "Ab dominant seventh 1st inversion": ["C", "Eb", "Gb", "Ab"],
    "Ab dominant seventh 2nd inversion": ["Eb", "Gb", "Ab", "C"],
    "Ab dominant seventh 3rd inversion": ["Gb", "Ab", "C", "Eb"],
    "A dominant seventh root": ["A", "C#", "E", "G"],
    "A dominant seventh 1st inversion": ["C#", "E", "G", "A"],
    "A dominant seventh 2nd inversion": ["E", "G", "A", "C#"],
    "A dominant seventh 3rd inversion": ["G", "A", "C#", "E"],
    "Bb dominant seventh root": ["Bb", "D", "F", "Ab"],
    "Bb dominant seventh 1st inversion": ["D", "F", "Ab", "Bb"],
    "Bb dominant seventh 2nd inversion": ["F", "Ab", "Bb", "D"],
    "Bb dominant seventh 3rd inversion": ["Ab", "Bb", "D", "F"],
    "B dominant seventh root": ["B", "D#", "F#", "A"],
    "B dominant seventh 1st inversion": ["D#", "F#", "A", "B"],
    "B dominant seventh 2nd inversion": ["F#", "A", "B", "D#"],
    "B dominant seventh 3rd inversion": ["A", "B", "D#", "F#"],

    # Minor sevenths
    "C minor seventh root": ["C", "Eb", "G", "Bb"],
    "C minor seventh 1st inversion": ["Eb", "G", "Bb", "C"],
    "C minor seventh 2nd inversion": ["G", "Bb", "C", "Eb"],
    "C minor seventh 3rd inversion": ["Bb", "C", "Eb", "G"],
    "C# minor seventh root": ["C#", "E", "G#", "B"],
    "C# minor seventh 1st inversion": ["E", "G#", "B", "C#"],
    "C# minor seventh 2nd inversion": ["G#", "B", "C#", "E"],
    "C# minor seventh 3rd inversion": ["B", "C#", "E", "G#"],
    "D minor seventh root": ["D", "F", "A", "C"],
    "D minor seventh 1st inversion": ["F", "A", "C", "D"],
    "D minor seventh 2nd inversion": ["A", "C", "D", "F"],
    "D minor seventh 3rd inversion": ["C", "D", "F", "A"],
    "Eb minor seventh root": ["Eb", "Gb", "Bb", "Db"],
    "Eb minor seventh 1st inversion": ["Gb", "Bb", "Db", "Eb"],
    "Eb minor seventh 2nd inversion": ["Bb", "Db", "Eb", "Gb"],
    "Eb minor seventh 3rd inversion": ["Db", "Eb", "Gb", "Bb"],
    "E minor seventh root": ["E", "G", "B", "D"],
    "E minor seventh 1st inversion": ["G", "B", "D", "E"],
    "E minor seventh 2nd inversion": ["B", "D", "E", "G"],
    "E minor seventh 3rd inversion": ["D", "E", "G", "B"],
    "F minor seventh root": ["F", "Ab", "C", "Eb"],
    "F minor seventh 1st inversion": ["Ab", "C", "Eb", "F"],
    "F minor seventh 2nd inversion": ["C", "Eb", "F", "Ab"],
    "F minor seventh 3rd inversion": ["Eb", "F", "Ab", "C"],
    "F# minor seventh root": ["F#", "A", "C#", "E"],
    "F# minor seventh 1st inversion": ["A", "C#", "E", "F#"],
    "F# minor seventh 2nd inversion": ["C#", "E", "F#", "A"],
    "F# minor seventh 3rd inversion": ["E", "F#", "A", "C#"],
    "G minor seventh root": ["G", "Bb", "D", "F"],
    "G minor seventh 1st inversion": ["Bb", "D", "F", "G"],
    "G minor seventh 2nd inversion": ["D", "F", "G", "Bb"],
    "G minor seventh 3rd inversion": ["F", "G", "Bb", "D"],
    "Ab minor seventh root": ["Ab", "Cb", "Eb", "Gb"],
    "Ab minor seventh 1st inversion": ["Cb", "Eb", "Gb", "Ab"],
    "Ab minor seventh 2nd inversion": ["Eb", "Gb", "Ab", "Cb"],
    "Ab minor seventh 3rd inversion": ["Gb", "Ab", "Cb", "Eb"],
    "A minor seventh root": ["A", "C", "E", "G"],
    "A minor seventh 1st inversion": ["C", "E", "G", "A"],
    "A minor seventh 2nd inversion": ["E", "G", "A", "C"],
    "A minor seventh 3rd inversion": ["G", "A", "C", "E"],
    "Bb minor seventh root": ["Bb", "Db", "F", "Ab"],
    "Bb minor seventh 1st inversion": ["Db", "F", "Ab", "Bb"],
    "Bb minor seventh 2nd inversion": ["F", "Ab", "Bb", "Db"],
    "Bb minor seventh 3rd inversion": ["Ab", "Bb", "Db", "F"],
    "B minor seventh root": ["B", "D", "F#", "A"],
    "B minor seventh 1st inversion": ["D", "F#", "A", "B"],
    "B minor seventh 2nd inversion": ["F#", "A", "B", "D"],
    "B minor seventh 3rd inversion": ["A", "B", "D", "F#"],

    # Minor seventh flat five (half-diminished)
    "C minor seventh flat five root": ["C", "Eb", "Gb", "Bb"],
    "C minor seventh flat five 1st inversion": ["Eb", "Gb", "Bb", "C"],
    "C minor seventh flat five 2nd inversion": ["Gb", "Bb", "C", "Eb"],
    "C minor seventh flat five 3rd inversion": ["Bb", "C", "Eb", "Gb"],
    "C# minor seventh flat five root": ["C#", "E", "G", "B"],
    "C# minor seventh flat five 1st inversion": ["E", "G", "B", "C#"],
    "C# minor seventh flat five 2nd inversion": ["G", "B", "C#", "E"],
    "C# minor seventh flat five 3rd inversion": ["B", "C#", "E", "G"],
    "D minor seventh flat five root": ["D", "F", "Ab", "C"],
    "D minor seventh flat five 1st inversion": ["F", "Ab", "C", "D"],
    "D minor seventh flat five 2nd inversion": ["Ab", "C", "D", "F"],
    "D minor seventh flat five 3rd inversion": ["C", "D", "F", "Ab"],
    "Eb minor seventh flat five root": ["Eb", "Gb", "Bbb", "Db"],
    "Eb minor seventh flat five 1st inversion": ["Gb", "Bbb", "Db", "Eb"],
    "Eb minor seventh flat five 2nd inversion": ["Bbb", "Db", "Eb", "Gb"],
    "Eb minor seventh flat five 3rd inversion": ["Db", "Eb", "Gb", "Bbb"],
    "E minor seventh flat five root": ["E", "G", "Bb", "D"],
    "E minor seventh flat five 1st inversion": ["G", "Bb", "D", "E"],
    "E minor seventh flat five 2nd inversion": ["Bb", "D", "E", "G"],
    "E minor seventh flat five 3rd inversion": ["D", "E", "G", "Bb"],
    "F minor seventh flat five root": ["F", "Ab", "Cb", "Eb"],
    "F minor seventh flat five 1st inversion": ["Ab", "Cb", "Eb", "F"],
    "F minor seventh flat five 2nd inversion": ["Cb", "Eb", "F", "Ab"],
    "F minor seventh flat five 3rd inversion": ["Eb", "F", "Ab", "Cb"],
    "F# minor seventh flat five root": ["F#", "A", "C", "E"],
    "F# minor seventh flat five 1st inversion": ["A", "C", "E", "F#"],
    "F# minor seventh flat five 2nd inversion": ["C", "E", "F#", "A"],
    "F# minor seventh flat five 3rd inversion": ["E", "F#", "A", "C"],
    "G minor seventh flat five root": ["G", "Bb", "Db", "F"],
    "G minor seventh flat five 1st inversion": ["Bb", "Db", "F", "G"],
    "G minor seventh flat five 2nd inversion": ["Db", "F", "G", "Bb"],
    "G minor seventh flat five 3rd inversion": ["F", "G", "Bb", "Db"],
    "Ab minor seventh flat five root": ["Ab", "Cb", "Ebb", "Gb"],
    "Ab minor seventh flat five 1st inversion": ["Cb", "Ebb", "Gb", "Ab"],
    "Ab minor seventh flat five 2nd inversion": ["Ebb", "Gb", "Ab", "Cb"],
    "Ab minor seventh flat five 3rd inversion": ["Gb", "Ab", "Cb", "Ebb"],
    "A minor seventh flat five root": ["A", "C", "Eb", "G"],
    "A minor seventh flat five 1st inversion": ["C", "Eb", "G", "A"],
    "A minor seventh flat five 2nd inversion": ["Eb", "G", "A", "C"],
    "A minor seventh flat five 3rd inversion": ["G", "A", "C", "Eb"],
    "Bb minor seventh flat five root": ["Bb", "Db", "Fb", "Ab"],
    "Bb minor seventh flat five 1st inversion": ["Db", "Fb", "Ab", "Bb"],
    "Bb minor seventh flat five 2nd inversion": ["Fb", "Ab", "Bb", "Db"],
    "Bb minor seventh flat five 3rd inversion": ["Ab", "Bb", "Db", "Fb"],
    "B minor seventh flat five root": ["B", "D", "F", "A"],
    "B minor seventh flat five 1st inversion": ["D", "F", "A", "B"],
    "B minor seventh flat five 2nd inversion": ["F", "A", "B", "D"],
    "B minor seventh flat five 3rd inversion": ["A", "B", "D", "F"],
    # ... (add all diminished chords similarly)
}

# --- MOBILE-FRIENDLY BUTTONS CSS ---
st.markdown("""
<style>
/* Shrink buttons on mobile */
@media (max-width: 600px) {
    div.stButton > button {
        padding: 4px 8px;
        font-size: 12px;
        margin-bottom: 4px;
    }
}
</style>
""", unsafe_allow_html=True)

# --- Group chords by base name ---
grouped_chords = defaultdict(list)
for chord_name in CHORDS.keys():
    words = chord_name.split()
    if "major" in words or "minor" in words or "diminished" in words:
        if "seventh" in chord_name or "flat five" in chord_name or "dominant" in chord_name:
            base = " ".join(words[:3])
        else:
            base = " ".join(words[:2])
    else:
        base = " ".join(words[:2])
    grouped_chords[base].append(chord_name)

# --- Sidebar selection ---
st.sidebar.title("Select Chords for Quiz")
selected_base_chords = []

categories = {"Major": [], "Minor": [], "Diminished": [], "Sevenths & Extensions": []}

for base in grouped_chords.keys():
    if "major" in base and "seventh" not in base:
        categories["Major"].append(base)
    elif "minor" in base and "seventh" not in base:
        categories["Minor"].append(base)
    elif "diminished" in base:
        categories["Diminished"].append(base)
    else:
        categories["Sevenths & Extensions"].append(base)

for cat in categories:
    categories[cat].sort()

for cat, bases in categories.items():
    with st.sidebar.expander(cat, expanded=True):
        for base in bases:
            if st.checkbox(base, value=base in ["C major", "A minor", "E minor", "G major"]):
                selected_base_chords.append(base)

if not selected_base_chords:
    st.warning("Please select at least one chord.")
    st.stop()

# --- Build selected chords dict ---
selected_chords_dict = {base: grouped_chords[base] for base in selected_base_chords}
all_selected_chords = [ch for sublist in selected_chords_dict.values() for ch in sublist]

if mode == "identify the position":
    # --- Initialize session state ---
    if "current_chord" not in st.session_state or st.session_state.current_chord not in all_selected_chords:
        st.session_state.current_chord = random.choice(all_selected_chords)

    if "attempts" not in st.session_state:
        st.session_state.attempts = {}

    if "show_result" not in st.session_state:
        st.session_state.show_result = False
    if "last_attempt" not in st.session_state:
        st.session_state.last_attempt = None

    # --- Next chord ---
    if st.button("Next Chord"):
        remaining_chords = [ch for ch in all_selected_chords if ch != st.session_state.current_chord]
        if remaining_chords:
            st.session_state.current_chord = random.choice(remaining_chords)
        st.session_state.attempts[st.session_state.current_chord] = []
        st.session_state.show_result = False
        st.session_state.last_attempt = None

    chord_key = st.session_state.current_chord
    st.write(f"### Notes: {', '.join(CHORDS[chord_key])}")

    # --- Handle button clicks ---
    def handle_option(option):
        clicked = st.button(option, key=f"{chord_key}_{option}")
        if clicked:
            if chord_key not in st.session_state.attempts:
                st.session_state.attempts[chord_key] = []
            if option not in st.session_state.attempts[chord_key]:
                st.session_state.attempts[chord_key].append(option)
            st.session_state.show_result = True
            st.session_state.last_attempt = option
        return clicked

    # --- Display columns of options with feedback ---
    sorted_bases = sorted(selected_base_chords)
    cols = st.columns(len(sorted_bases))

    for col_idx, base in enumerate(sorted_bases):
        with cols[col_idx]:
            st.write(f"**{base}**")
            options = selected_chords_dict[base]

            # Root chord first
            root_options = [opt for opt in options if "root" in opt.lower()]
            other_options = [opt for opt in options if "root" not in opt.lower()]
            options_sorted = root_options + sorted(other_options)

            for option in options_sorted:
                handle_option(option)

                # Feedback coloring for attempted options
                attempts = st.session_state.attempts.get(chord_key, [])
                if option in attempts:
                    if option == chord_key:
                        st.success(f"{option} ✅")
                    else:
                        st.error(f"{option} ❌")

    # --- Display bottom feedback ---
    attempts = st.session_state.attempts.get(chord_key, [])
    if attempts and st.session_state.last_attempt:
        if st.session_state.last_attempt == chord_key:
            st.success(f"✅ Correct! It was {chord_key}")
        else:
            st.error(f"❌ Incorrect. Try again!")

elif mode == "Playing the Position":
    # --- PLAYING THE POSITION MODE ---
    if not selected_base_chords:
        st.warning("Please select at least one chord.")
        st.stop()

    # Pick a random chord for question
    current_chord = random.choice(all_selected_chords)
    st.write(f"### Which diagram shows: {current_chord}?")

    # --- Generate keyboard images ---
    def generate_keyboard_image(highlight_notes, keys_visible=25):
        """
        Generates a 25-key segment of a keyboard with black and white keys correctly positioned.
        highlight_notes should be note names like ['C', 'E', 'G'].
        """
        key_order = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]

        # Generate the 25 keys in order
        keyboard_notes = []
        octave = 0
        while len(keyboard_notes) < keys_visible:
            for note in key_order:
                keyboard_notes.append(f"{note}{octave}")
                if len(keyboard_notes) >= keys_visible:
                    break
            octave += 1

        img_width, img_height = 500, 120
        white_key_height = img_height
        black_key_height = int(img_height * 0.6)

        # Count white keys for width
        white_keys = [note for note in keyboard_notes if "#" not in note]
        white_key_width = img_width / len(white_keys)

        img = Image.new("RGB", (img_width, img_height), "white")
        draw = ImageDraw.Draw(img)

        # Draw white keys
        white_key_positions = {}
        x = 0
        for note in keyboard_notes:
            if "#" not in note:
                color = "yellow" if note[:-1] in highlight_notes else "white"
                draw.rectangle([x, 0, x + white_key_width, white_key_height], fill=color, outline="black")
                white_key_positions[note] = x
                x += white_key_width

        # Draw black keys
        for idx, note in enumerate(keyboard_notes):
            if "#" in note:
                # Black keys sit between white keys
                left_note_idx = idx - 1
                if keyboard_notes[left_note_idx] in white_key_positions:
                    x0 = white_key_positions[keyboard_notes[left_note_idx]] + white_key_width * 0.65
                    x1 = x0 + white_key_width * 0.7
                    color = "yellow" if note[:-1] in highlight_notes else "black"
                    draw.rectangle([x0, 0, x1, black_key_height], fill=color, outline="black")

        return img


    # --- Prepare answer options ---
    correct_notes = CHORDS[current_chord]
    correct_img = generate_keyboard_image(correct_notes)

    # Pick up to 3 wrong chords
    other_chords = [ch for ch in all_selected_chords if ch != current_chord]
    wrong_chords = random.sample(other_chords, min(3, len(other_chords)))
    wrong_imgs = [generate_keyboard_image(CHORDS[ch]) for ch in wrong_chords]

    # Combine correct and wrong options, then shuffle
    options = [(current_chord, correct_img)] + list(zip(wrong_chords, wrong_imgs))
    random.shuffle(options)

    # --- Display images with selection buttons ---
    cols = st.columns(len(options))
    clicked_option = None
    for idx, (chord_name, img) in enumerate(options):
        with cols[idx]:
            st.image(img)
            if st.button("Select", key=f"play_{chord_name}"):
                clicked_option = chord_name

    # --- Feedback ---
    if clicked_option:
        if clicked_option == current_chord:
            st.success(f"✅ Correct! It was {current_chord}")
        else:
            st.error(f"❌ Incorrect. It was {current_chord}")