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
# Draw piano
# -------------------
def draw_keyboard(chord_midis, start_note="C3", end_note="C5"):
    # chord_midis should be MIDI ints (you already convert with note_name_to_midi)
    start = note_name_to_midi(start_note)
    end = note_name_to_midi(end_note)

    WHITE_SEMITONES = {0, 2, 4, 5, 7, 9, 11}   # C D E F G A B
    BLACK_AFTER_WHITE = {0, 2, 5, 7, 9}        # C, D, F, G, A (their sharps)

    # Map each WHITE key in range to an x position (one unit per white key)
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

    # Draw white keys (base layer)
    for m in white_order:
        wx = white_midi_to_x[m]
        face = "yellow" if m in chord_set else "white"
        ax.add_patch(plt.Rectangle((wx, 0), white_w, white_h, facecolor=face, edgecolor="black", zorder=1))

    # Draw black keys (overlay, positioned between adjacent whites)
    for m in white_order:
        if (m % 12) in BLACK_AFTER_WHITE:
            b = m + 1  # the sharp right after this white
            if start <= b <= end:
                wx = white_midi_to_x[m]
                # center the black key between this white and the next white
                bx = wx + 1 - black_w / 2
                face = "red" if b in chord_set else "black"
                ax.add_patch(plt.Rectangle((bx, white_h - black_h), black_w, black_h,
                                           facecolor=face, edgecolor="black", zorder=2))

    ax.set_xlim(0, len(white_order))
    ax.set_ylim(0, white_h)
    ax.axis("off")
    st.pyplot(fig)

# -------------------
# Generate chord notes
# -------------------
def get_chord_notes(root, intervals, inversion):
    notes = [(root + i) % 12 for i in intervals]  # triad
    # reorder for inversion
    order = INVERSIONS[inversion]
    notes = [notes[i] for i in order]

    # expand onto 25-key keyboard (C to C, 2 octaves)
    all_notes = []
    for n in notes:
        for octave in [0, 12]:
            if 0 <= n + octave < 25:
                all_notes.append(n + octave)
    return sorted(all_notes)

# -------------------
# Streamlit app
# -------------------
st.title("Chord Trainer")

# chord selection
selected_chords = st.multiselect("Select chords to practice", list(CHORDS.keys()), default=list(CHORDS.keys()))

mode = st.radio("Mode", ["Name → Picture", "Picture → Name"])

if "question" not in st.session_state:
    st.session_state.question = None

if mode == "Name → Picture":
    if st.button("New Question") or st.session_state.question is None:
        chord = random.choice(selected_chords)
        inversion = random.choice(list(INVERSIONS.keys()))
        st.session_state.question = (chord, inversion)

    chord, inversion = st.session_state.question
    st.write(f"Which diagram shows **{chord} ({inversion})**?")

    # correct answer
    root = list(CHORDS.keys()).index(chord) * 2  # quick hack mapping
    notes = get_chord_notes(root, CHORDS[chord], inversion)
    correct_img = notes

    # wrong answers
    options = []
    for _ in range(3):
        other_chord = random.choice(selected_chords)
        other_inversion = random.choice(list(INVERSIONS.keys()))
        notes_wrong = get_chord_notes(list(CHORDS.keys()).index(other_chord)*2, CHORDS[other_chord], other_inversion)
        options.append((other_chord, other_inversion, notes_wrong))

    # shuffle all
    answers = [(chord, inversion, correct_img)] + options
    random.shuffle(answers)

    for i, (c, inv, notes) in enumerate(answers):
        st.write(f"Option {i+1}: {c} {inv}")
        draw_keyboard(notes)

