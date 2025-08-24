import streamlit as st
import matplotlib.pyplot as plt
import random

# -------------------
# Chord definitions
# -------------------
CHORDS = {
    "C major": [0, 4, 7],
    "A minor": [9, 0, 4],
    "G major": [7, 11, 2],
    "E minor": [4, 7, 11]
}

INVERSIONS = {
    "root": [0, 1, 2],
    "1st": [1, 2, 0],
    "2nd": [2, 0, 1]
}

# -------------------
# Note to MIDI
# -------------------
SEMI_TO_NOTE = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
NOTE_TO_SEMI = {n: i for i, n in enumerate(SEMI_TO_NOTE)}

def note_name_to_midi(note_name, octave=4):
    if note_name not in NOTE_TO_SEMI:
        raise ValueError(f"Invalid note name: {note_name}")
    return 12 * octave + NOTE_TO_SEMI[note_name]

def midi_to_note_name(midi):
    octave = midi // 12
    note = SEMI_TO_NOTE[midi % 12]
    return f"{note}{octave}"

# -------------------
# Build chord MIDI notes
# -------------------
def build_chord_midi(root_note, quality, inversion, base_octave=4):
    root_midi = note_name_to_midi(root_note, base_octave)
    intervals = CHORDS[root_note + (" major" if quality=="major" else " minor")] if root_note in CHORDS else CHORDS[quality]
    # Apply intervals
    notes = [root_midi + i for i in intervals]
    # Apply inversion
    order = INVERSIONS[inversion]
    notes = [notes[i] for i in order]
    return notes

# -------------------
# Draw keyboard
# -------------------
def draw_keyboard(chord_midis, start_note="C3", end_note="C5"):
    start = note_name_to_midi(start_note[:-1], int(start_note[-1]))
    end = note_name_to_midi(end_note[:-1], int(end_note[-1]))

    WHITE_SEMITONES = {0, 2, 4, 5, 7, 9, 11}
    BLACK_AFTER_WHITE = {0, 2, 5, 7, 9}  # C,D,F,G,A (their sharps)

    # Map white keys to x positions
    white_midi_to_x = {}
    white_order = []
    x = 0
    for m in range(start, end+1):
        if m % 12 in WHITE_SEMITONES:
            white_midi_to_x[m] = x
            white_order.append(m)
            x += 1

    # Draw keys
    white_w, white_h = 1.0, 4.0
    black_w, black_h = 0.6, 2.6

    fig, ax = plt.subplots(figsize=(10, 3))
    chord_set = set(chord_midis)

    # White keys
    for m in white_order:
        wx = white_midi_to_x[m]
        face = "yellow" if m in chord_set else "white"
        ax.add_patch(plt.Rectangle((wx, 0), white_w, white_h, facecolor=face, edgecolor="black", zorder=1))

    # Black keys
    for m in white_order:
        if (m % 12) in BLACK_AFTER_WHITE:
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
# Generate question
# -------------------
def generate_question(selected_chords):
    chord_name = random.choice(selected_chords)
    root_options = chord_name.split()[0]  # "C" from "C major"
    root_note = root_options
    quality = "major" if "major" in chord_name else "minor"
    inversion = random.choice(list(INVERSIONS.keys()))
    # Build MIDI notes (use octave 4 as base)
    midi_notes = build_chord_midi(root_note, quality, inversion, base_octave=4)
    return chord_name, root_note, quality, inversion, midi_notes

# -------------------
# Streamlit app
# -------------------
st.title("🎹 Chord Trainer")

selected_chords = st.multiselect("Select chords to practice", list(CHORDS.keys()), default=list(CHORDS.keys()))
mode = st.radio("Mode", ["Name → Picture", "Picture → Name"])

if "question" not in st.session_state:
    st.session_state.question = None
    st.session_state.feedback = ""

if st.button("Next Question") or st.session_state.question is None:
    if selected_chords:
        st.session_state.question = generate_question(selected_chords)
        st.session_state.feedback = ""

if st.session_state.question:
    chord_name, root_note, quality, inversion, midi_notes = st.session_state.question

    if mode == "Name → Picture":
        st.write(f"**Which diagram shows this chord?**")
        draw_keyboard(midi_notes)
        guess = st.text_input("Your Answer (e.g. C major (root))")
        if guess:
            if guess.strip().lower() == f"{chord_name} ({inversion})".lower():
                st.success("✅ Correct!")
            else:
                st.error(f"❌ Wrong. Correct answer: {chord_name} ({inversion})")

    elif mode == "Picture → Name":
        st.write("**Select the correct chord diagram**")
        # Generate 3 wrong options
        options = [(chord_name, inversion, midi_notes)]
        while len(options) < 4:
            wrong_chord = random.choice(selected_chords)
            wrong_root = wrong_chord.split()[0]
            wrong_quality = "major" if "major" in wrong_chord else "minor"
            wrong_inversion = random.choice(list(INVERSIONS.keys()))
            wrong_notes = build_chord_midi(wrong_root, wrong_quality, wrong_inversion, base_octave=4)
            if all(n not in midi_notes for n in wrong_notes):
                options.append((wrong_chord, wrong_inversion, wrong_notes))
        random.shuffle(options)

        cols = st.columns(2)
        for i, (c, inv, notes) in enumerate(options):
            with cols[i % 2]:
                draw_keyboard(notes)
                if st.button(f"Select Option {i+1}", key=f"opt{i}"):
                    if c == chord_name and inv == inversion:
                        st.success("✅ Correct!")
                    else:
                        st.error(f"❌ Wrong. Correct answer: {chord_name} ({inversion})")
                    st.session_state.question = None

