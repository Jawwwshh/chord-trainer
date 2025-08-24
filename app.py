import streamlit as st
import random
import matplotlib.pyplot as plt

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
# Note helpers
# -------------------
SEMI_TO_NOTE = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
NOTE_TO_SEMI = {n: i for i, n in enumerate(SEMI_TO_NOTE)}

def note_name_to_midi(note):
    """Convert note name (e.g., C3) to MIDI number"""
    name, octave = note[:-1], int(note[-1])
    return NOTE_TO_SEMI[name] + 12 * octave

# -------------------
# Draw piano keyboard
# -------------------
def draw_keyboard(chord_midis, start_note="C3", end_note="C5"):
    start = note_name_to_midi(start_note)
    end = note_name_to_midi(end_note)

    WHITE_SEMITONES = {0, 2, 4, 5, 7, 9, 11}   # C D E F G A B
    BLACK_AFTER_WHITE = {0, 2, 5, 7, 9}        # C, D, F, G, A (their sharps)

    # Map each white key to x position
    white_midi_to_x = {}
    white_order = []
    x = 0
    for m in range(start, end + 1):
        if m % 12 in WHITE_SEMITONES:
            white_midi_to_x[m] = x
            white_order.append(m)
            x += 1

    # Figure sizing
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
        if (m % 12) in BLACK_AFTER_WHITE:
            b = m + 1  # sharp immediately after white
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
# Generate chord notes (MIDI numbers)
# -------------------
def get_chord_notes(root_midi, intervals, inversion):
    notes = [(root_midi + i) for i in intervals]
    order = INVERSIONS[inversion]
    notes = [notes[i] for i in order]

    # Ensure notes fit inside C3–C5
    for i in range(len(notes)):
        while notes[i] < note_name_to_midi("C3"):
            notes[i] += 12
        while notes[i] > note_name_to_midi("C5"):
            notes[i] -= 12
    return sorted(notes)

# -------------------
# Streamlit app
# -------------------
st.title("🎹 Chord Trainer")

selected_chords = st.multiselect("Select chords to practice", list(CHORDS.keys()), default=list(CHORDS.keys()))
mode = st.radio("Mode", ["Name → Picture", "Picture → Name"])

if "question" not in st.session_state:
    st.session_state.question = None

# New question button
if st.button("New Question") or st.session_state.question is None:
    chord = random.choice(selected_chords)
    inversion = random.choice(list(INVERSIONS.keys()))
    st.session_state.question = (chord, inversion)

chord, inversion = st.session_state.question
st.write(f"Which diagram shows **{chord} ({inversion})**?")

# correct answer
root_midi = note_name_to_midi(chord[0] + "4")  # simple root note in octave 4
correct_notes = get_chord_notes(root_midi, CHORDS[chord], inversion)

# wrong answers
options = []
for _ in range(3):
    other_chord = random.choice(selected_chords)
    other_inversion = random.choice(list(INVERSIONS.keys()))
    other_root = note_name_to_midi(other_chord[0] + "4")
    wrong_notes = get_chord_notes(other_root, CHORDS[other_chord], other_inversion)
    options.append((other_chord, other_inversion, wrong_notes))

# shuffle
answers = [(chord, inversion, correct_notes)] + options
random.shuffle(answers)

for i, (c, inv, notes) in enumerate(answers):
    st.write(f"Option {i+1}: {c} ({inv})")
    draw_keyboard(notes)
