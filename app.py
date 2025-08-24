import streamlit as st
import matplotlib.pyplot as plt
import random

# -------------------
# Note & chord definitions
# -------------------
SEMI_TO_NOTE = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
NOTE_TO_SEMI = {n: i for i, n in enumerate(SEMI_TO_NOTE)}

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

# -------------------
# MIDI conversion
# -------------------
def note_name_to_midi(note_name, octave=4):
    """Convert note name (with optional sharp) + octave to MIDI number"""
    semitone = NOTE_TO_SEMI.index(note_name)
    return 12 * octave + semitone

def midi_to_note_name(midi):
    octave = midi // 12
    name = SEMI_TO_NOTE[midi % 12]
    return f"{name}{octave}"

# -------------------
# Build chord in MIDI numbers
# -------------------
def build_chord_midi(root_note, quality="major", inversion="root", base_octave=4):
    """Return list of MIDI numbers for a triad with given inversion"""
    root_midi = note_name_to_midi(root_note, base_octave)
    intervals = CHORD_STRUCTURES[quality]
    notes = [root_midi + i for i in intervals]
    # apply inversion
    order = INVERSIONS[inversion]
    notes = [notes[i] for i in order]
    # make sure lowest note is in C3–C5 range
    while min(notes) > note_name_to_midi("C5"):
        notes = [n - 12 for n in notes]
    while max(notes) < note_name_to_midi("C3"):
        notes = [n + 12 for n in notes]
    return notes

# -------------------
# Draw keyboard
# -------------------
def draw_keyboard(chord_midis, start_note="C3", end_note="C5"):
    start = note_name_to_midi(start_note, 3)
    end = note_name_to_midi(end_note, 5)

    WHITE_SEMITONES = {0, 2, 4, 5, 7, 9, 11}
    BLACK_AFTER_WHITE = {0, 2, 5, 7, 9}

    # Map white keys to x positions
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
            b = m + 1
            if start <= b <= end:
                wx = white_midi_to_x[m]
                bx = wx + 1 - black_w / 2
                face = "red" if b in chord_set else "black"
                ax.add_patch(plt.Rectangle((bx, white_h - black_h), black_w, black_h,
                                           facecolor=face, edgecolor="black", zorder=2))

    ax.set_xlim(0, len(white_order))
    ax.set_ylim(0, white_h)
    ax.axis("off")
    st.pyplot(fig)

# -------------------
# Streamlit app
# -------------------
st.title("🎹 Chord Trainer")

selected_chords = st.multiselect("Select chords to practice", list(KEYS.keys()), default=["C major","A minor","G major","E minor"])
mode = st.radio("Mode", ["Name → Picture", "Picture → Name"])

if "question" not in st.session_state:
    st.session_state.question = None
    st.session_state.feedback = ""

def generate_question():
    chord_name = random.choice(selected_chords)
    root_options = KEYS[chord_name]
    root_note = random.choice(root_options)
    quality = "major" if "major" in chord_name else "minor"
    inversion = random.choice(list(INVERSIONS.keys()))
    midi_notes = build_chord_midi(root_note, quality, inversion)
    return (chord_name, root_note, quality, inversion, midi_notes)

# Generate new question
if st.button("New Question") or st.session_state.question is None:
    if selected_chords:
        st.session_state.question = generate_question()
        st.session_state.feedback = ""

if st.session_state.question:
    chord_name, root_note, quality, inversion, chord_midis = st.session_state.question
    if mode == "Name → Picture":
        st.write(f"Which diagram shows the chord?")
        draw_keyboard(chord_midis)
    elif mode == "Picture → Name":
        st.write(f"Identify the chord:")

        # Correct answer
        correct = (chord_name, root_note, quality, inversion, chord_midis)

        # Generate 3 wrong options
        options = [correct]
        while len(options) < 4:
            wrong = generate_question()
            if wrong not in options:
                options.append(wrong)
        random.shuffle(options)

        cols = st.columns(2)
        for i, opt in enumerate(options):
            _, _, _, _, midi_notes = opt
            with cols[i % 2]:
                draw_keyboard(midi_notes)
                if st.button(f"Select Option {i+1}", key=f"opt{i}"):
                    if opt == correct:
                        st.session_state.feedback = "✅ Correct!"
                    else:
                        st.session_state.feedback = f"❌ Wrong! Correct answer: {correct[0]}"

if st.session_state.feedback:
    st.write(st.session_state.feedback)

