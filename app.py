import streamlit as st
import matplotlib.pyplot as plt
import random

# -------------------
# Chord definitions (triads on white keys only)
# -------------------
CHORDS = {
    "C major": ["C", "E", "G"],
    "A minor": ["A", "C", "E"],
    "G major": ["G", "B", "D"],
    "E minor": ["E", "G", "B"]
}

INVERSIONS = {
    "root": [0, 1, 2],
    "1st": [1, 2, 0],
    "2nd": [2, 0, 1]
}

SEMI_TO_NOTE = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
NOTE_TO_SEMI = {n:i for i,n in enumerate(SEMI_TO_NOTE)}

# Keyboard range
WHITE_KEYS_ORDER = ["C","D","E","F","G","A","B"]
KEYBOARD_START = 48  # C3
KEYBOARD_END = 72    # C5

# -------------------
# Helpers
# -------------------
def note_to_midi(note_name, octave):
    return NOTE_TO_SEMI[note_name] + 12 * octave

def chord_to_midi(chord_notes, inversion="root", base_octave=4):
    # reorder notes for inversion
    order = INVERSIONS[inversion]
    notes_ordered = [chord_notes[i] for i in order]
    # convert to MIDI
    midi_notes = [note_to_midi(n, base_octave) for n in notes_ordered]
    # center the chord inside C3-C5
    min_note = min(midi_notes)
    max_note = max(midi_notes)
    if min_note < KEYBOARD_START:
        midi_notes = [n+12 for n in midi_notes]
    if max_note > KEYBOARD_END:
        midi_notes = [n-12 for n in midi_notes]
    return midi_notes

# -------------------
# Draw keyboard
# -------------------
def draw_keyboard(chord_midis):
    WHITE_SEMITONES = {0,2,4,5,7,9,11}
    BLACK_AFTER_WHITE = {0,2,5,7,9}  # positions with black keys after

    # white keys positions
    white_order = []
    white_x_map = {}
    x = 0
    for m in range(KEYBOARD_START, KEYBOARD_END+1):
        if m % 12 in WHITE_SEMITONES:
            white_order.append(m)
            white_x_map[m] = x
            x += 1

    fig, ax = plt.subplots(figsize=(10,3))
    white_w, white_h = 1.0, 4.0
    black_w, black_h = 0.6, 2.6
    chord_set = set(chord_midis)

    # draw white keys
    for m in white_order:
        wx = white_x_map[m]
        face = "yellow" if m in chord_set else "white"
        ax.add_patch(plt.Rectangle((wx,0), white_w, white_h, facecolor=face, edgecolor="black", zorder=1))

    # draw black keys (never highlight them)
    for m in white_order:
        if m % 12 in BLACK_AFTER_WHITE:
            b = m + 1
            if KEYBOARD_START <= b <= KEYBOARD_END:
                wx = white_x_map[m]
                bx = wx + 1 - black_w/2
                ax.add_patch(plt.Rectangle((bx, white_h-black_h), black_w, black_h, facecolor="black", edgecolor="black", zorder=2))

    ax.set_xlim(0, len(white_order))
    ax.set_ylim(0, white_h)
    ax.axis("off")
    st.pyplot(fig)

# -------------------
# Generate and display question safely
# -------------------
if not selected_chords:
    st.warning("Please select at least one chord to practice.")
else:
    # generate new question if none exists or button pressed
    if "question" not in st.session_state or st.session_state.question is None or st.button("Next Question"):
        options, correct = generate_question(selected_chords)
        st.session_state.options = options
        st.session_state.question = correct
        st.session_state.feedback = ""

    q = st.session_state.question

    if q is not None:
        if mode == "Name → Picture":
            st.write(f"Which diagram shows **{q[0]} ({q[1]})**?")
            draw_keyboard(q[2])
        elif mode == "Picture → Name":
            st.write("Which diagram matches the chord shown?")
            cols = st.columns(2)
            for i, (name, inversion, midi) in enumerate(st.session_state.options):
                with cols[i % 2]:
                    draw_keyboard(midi)
                    if st.button(f"Select Option {i+1}", key=f"opt{i}"):
                        if (name, inversion, midi) == q:
                            st.session_state.feedback = "✅ Correct!"
                        else:
                            st.session_state.feedback = f"❌ Wrong! Correct: {q[0]} ({q[1]})"
                        st.session_state.question = None

    if st.session_state.feedback:
        st.write(st.session_state.feedback)

# -------------------
# Streamlit app
# -------------------
st.title("🎹 Chord Trainer")

selected_chords = st.multiselect("Select chords to practice", list(CHORDS.keys()), default=list(CHORDS.keys()))
mode = st.radio("Mode", ["Name → Picture", "Picture → Name"])

if "question" not in st.session_state:
    st.session_state.question = None
    st.session_state.options = []
    st.session_state.feedback = ""

if st.button("Next Question") or st.session_state.question is None:
    options, correct = generate_question(selected_chords)
    st.session_state.options = options
    st.session_state.question = correct
    st.session_state.feedback = ""

q = st.session_state.question

if mode == "Name → Picture":
    st.write(f"Which diagram shows **{q[0]} ({q[1]})**?")
    draw_keyboard(q[2])

elif mode == "Picture → Name":
    st.write("Which diagram matches the chord shown?")
    cols = st.columns(2)
    for i, (name, inversion, midi) in enumerate(st.session_state.options):
        with cols[i % 2]:
            draw_keyboard(midi)
            if st.button(f"Select Option {i+1}", key=f"opt{i}"):
                if (name, inversion, midi) == q:
                    st.session_state.feedback = "✅ Correct!"
                else:
                    st.session_state.feedback = f"❌ Wrong! Correct: {q[0]} ({q[1]})"
                st.session_state.question = None

if st.session_state.feedback:
    st.write(st.session_state.feedback)

