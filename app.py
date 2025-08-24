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
def draw_keyboard(highlight_notes):
    fig, ax = plt.subplots(figsize=(8, 3))
    white_keys = list(range(25))
    black_keys = [1, 3, 6, 8, 10, 13, 15, 18, 20, 22]

    # Draw white keys
    for i in white_keys:
        color = "yellow" if i in highlight_notes else "white"
        ax.add_patch(plt.Rectangle((i, 0), 1, 4, facecolor=color, edgecolor="black"))

    # Draw black keys
    for i in black_keys:
        if 0 <= i < 25:
            color = "red" if i in highlight_notes else "black"
            ax.add_patch(plt.Rectangle((i - 0.3, 2), 0.6, 2, facecolor=color, edgecolor="black"))

    ax.set_xlim(0, 25)
    ax.set_ylim(0, 4)
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

