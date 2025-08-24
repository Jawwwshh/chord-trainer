import streamlit as st
import matplotlib.pyplot as plt
import random

# -------------------
# Chord definitions
# -------------------
CHORD_STRUCTURES = {
    "major": [0, 4, 7],
    "minor": [0, 3, 7]
}

INVERSIONS = {
    "root": [0, 1, 2],
    "1st": [1, 2, 0],
    "2nd": [2, 0, 1]
}

KEYS = {
    "C major": ["C", "D", "E", "F", "G", "A", "B"],
    "A minor": ["A", "B", "C", "D", "E", "F", "G"],
    "G major": ["G", "A", "B", "C", "D", "E", "F#"],
    "E minor": ["E", "F#", "G", "A", "B", "C", "D"]
}

SEMI_TO_NOTE = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
NOTE_TO_SEMI = {n: i for i, n in enumerate(SEMI_TO_NOTE)}

# -------------------
# Note utilities
# -------------------
def note_name_to_midi(note):
    """Convert note name (e.g., C4) to MIDI number."""
    name, octave = note[:-1], int(note[-1])
    return NOTE_TO_SEMI[name] + 12 * octave

def midi_to_note_name(midi):
    octave = midi // 12
    name = SEMI_TO_NOTE[midi % 12]
    return f"{name}{octave}"

def build_chord_midi(root_note, quality, inversion="root"):
    """Return a list of MIDI numbers for a chord, centered around C4."""
    root_midi = note_name_to_midi(root_note + "4")  # start near middle C
    intervals = CHORD_STRUCTURES[quality]
    notes = [root_midi + i for i in intervals]
    
    # Apply inversion
    order = INVERSIONS[inversion]
    notes = [notes[i] for i in order]
    for j in range(order[0]):
        notes[j] += 12  # push lowest notes up an octave

    # Center chord in C3–C5
    lowest = min(notes)
    highest = max(notes)
    mid = (lowest + highest) // 2
    shift = note_name_to_midi("C4") - mid
    notes = [n + shift for n in notes]

    # Clip to C3–C5
    notes = [n for n in notes if note_name_to_midi("C3") <= n <= note_name_to_midi("C5")]
    return notes

# -------------------
# Draw piano
# -------------------
def draw_keyboard(chord_midis):
    """Draw a 25-key piano keyboard (C3–C5) highlighting chord_midis."""
    start = note_name_to_midi("C3")
    end = note_name_to_midi("C5")
    
    WHITE_SEMITONES = {0, 2, 4, 5, 7, 9, 11}
    BLACK_AFTER_WHITE = {0, 2, 5, 7, 9}  # C, D, F, G, A

    # Map white keys to positions
    white_midi_to_x = {}
    white_order = []
    x = 0
    for m in range(start, end + 1):
        if m % 12 in WHITE_SEMITONES:
            white_midi_to_x[m] = x
            white_order.append(m)
            x += 1

    white_w, white_h = 1.0, 4.0
    black_w, black_h = 0.6, 2.6

    fig, ax = plt.subplots(figsize=(10, 3))
    chord_set = set(chord_midis)

    # Draw white keys
    for m in white_order:
        wx = white_midi_to_x[m]
        face = "yellow" if m in chord_set else "white"
        ax.add_patch(plt.Rectangle((wx, 0), white_w, white_h, facecolor=face, edgecolor="black", zorder=1))

    # Draw black keys
    for m in white_order:
        if m % 12 in BLACK_AFTER_WHITE:
            b = m + 1  # the sharp after this white
            if start <= b <= end:
                wx = white_midi_to_x[m]
                bx = wx + 1 - black_w / 2
                face = "red" if b in chord_set else "black"
                ax.add_patch(plt.Rectangle((bx, white_h - black_h), black_w, black_h, facecolor=face, edgecolor="black", zorder=2))

    ax.set_xlim(0, len(white_order))
    ax.set_ylim(0, white_h)
    ax.axis("off")
    st.pyplot(fig)

# -------------------
# Streamlit app
# -------------------
st.title("🎹 Chord Trainer")

selected_chords = st.multiselect(
    "Select chords to practice", list(KEYS.keys()), default=list(KEYS.keys())
)

mode = st.radio("Mode", ["Name → Picture", "Picture → Name"])

if "quiz" not in st.session_state:
    st.session_state.quiz = None
    st.session_state.feedback = ""

# Generate new question
if st.button("New Question") or st.session_state.quiz is None:
    if selected_chords:
        chord_name = random.choice(selected_chords)
        scale = KEYS[chord_name]
        root_note = random.choice(scale)
        quality = "major" if "major" in chord_name else "minor"
        inversion = random.choice(list(INVERSIONS.keys()))
        chord_midis = build_chord_midi(root_note, quality, inversion)

        # Build 3 wrong options
        options = []
        while len(options) < 3:
            wrong_chord = random.choice(selected_chords)
            wrong_scale = KEYS[wrong_chord]
            wrong_root = random.choice(wrong_scale)
            wrong_quality = "major" if "major" in wrong_chord else "minor"
            wrong_inversion = random.choice(list(INVERSIONS.keys()))
            wrong_midis = build_chord_midi(wrong_root, wrong_quality, wrong_inversion)
            if wrong_midis != chord_midis:
                options.append(wrong_midis)

        all_options = options + [chord_midis]
        random.shuffle(all_options)
        st.session_state.quiz = {
            "correct": chord_midis,
            "all_options": all_options,
            "chord_name": chord_name,
            "root": root_note,
            "quality": quality,
            "inversion": inversion
        }
        st.session_state.feedback = ""

# Display question
if st.session_state.quiz:
    q = st.session_state.quiz
    if mode == "Name → Picture":
        st.write(f"Which picture shows **{q['chord_name']} ({q['inversion']})**?")
        for i, option in enumerate(q["all_options"]):
            st.write(f"Option {i+1}")
            draw_keyboard(option)
    else:  # Picture → Name
        st.write("Which chord is this?")
        for i, option in enumerate(q["all_options"]):
            draw_keyboard(option)
            if st.button(f"Option {i+1}", key=f"opt{i}"):
                if option == q["correct"]:
                    st.session_state.feedback = f"✅ Correct! It was {q['chord_name']} ({q['inversion']})"
                else:
                    st.session_state.feedback = f"❌ Wrong! It was {q['chord_name']} ({q['inversion']})"
                st.session_state.quiz = None

# Feedback
if st.session_state.feedback:
    st.write(st.session_state.feedback)
