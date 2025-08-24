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
KEYBOARD_START = 48  # C3
KEYBOARD_END = 72    # C5
WHITE_SEMITONES = {0,2,4,5,7,9,11}  # white keys only

# -------------------
# Helpers
# -------------------
def note_to_midi(note_name, octave):
    """Convert note name + octave to MIDI number."""
    return NOTE_TO_SEMI[note_name] + 12 * octave

def chord_to_midi(chord_notes, inversion="root", base_octave=4):
    """Convert chord (white keys) to MIDI numbers, apply inversion, and center on keyboard."""
    order = INVERSIONS[inversion]
    notes_ordered = [chord_notes[i] for i in order]
    midi_notes = [note_to_midi(n, base_octave) for n in notes_ordered]

    # Center chord inside C3-C5
    min_note = min(midi_notes)
    max_note = max(midi_notes)
    while min_note < KEYBOARD_START:
        midi_notes = [n+12 for n in midi_notes]
        min_note = min(midi_notes)
        max_note = max(midi_notes)
    while max_note > KEYBOARD_END:
        midi_notes = [n-12 for n in midi_notes]
        min_note = min(midi_notes)
        max_note = max(midi_notes)

    return midi_notes

# -------------------
# Draw keyboard
# -------------------
def draw_keyboard(chord_midis):
    """Draw a piano keyboard (C3–C5) with highlighted white keys."""
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

    # Draw white keys
    for m in white_order:
        wx = white_x_map[m]
        face = "yellow" if m in chord_set else "white"
        ax.add_patch(plt.Rectangle((wx,0), white_w, white_h, facecolor=face, edgecolor="black", zorder=1))

    # Draw black keys (never highlight them)
    BLACK_AFTER_WHITE = {0,2,5,7,9}
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
# Generate question and options
# -------------------
def generate_question(selected_chords):
    """Return 4 options and the correct answer."""
    correct_name = random.choice(selected_chords)
    inversion = random.choice(list(INVERSIONS.keys()))
    correct_midi = chord_to_midi(CHORDS[correct_name], inversion)

    # Generate 3 wrong options
    options = [(correct_name, inversion, correct_midi)]
    while len(options) < 4:
        wrong_name = random.choice(selected_chords)
        wrong_inversion = random.choice(list(INVERSIONS.keys()))
        wrong_midi = chord_to_midi(CHORDS[wrong_name], wrong_inversion)
        if all(wrong_midi != o[2] for o in options):
            options.append((wrong_name, wrong_inversion, wrong_midi))

    random.shuffle(options)
    return options, (correct_name, inversion, correct_midi)

# -------------------
# Streamlit App
# -------------------
st.title("🎹 Chord Trainer")

selected_chords = st.multiselect("Select chords to practice", list(CHORDS.keys()), default=list(CHORDS.keys()))
mode = st.radio("Mode", ["Name → Picture", "Picture → Name"])

if "question" not in st.session_state:
    st.session_state.question = None
    st.session_state.options = []
    st.session_state.feedback = ""

# Safety: at least one chord selected
if not selected_chords:
    st.warning("Please select at least one chord to practice.")
else:
    # Generate new question if none exists or button pressed
    if st.button("Next Question") or st.session_state.question is None:
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
            cols = st.columns(4)  # 4 options
            for i, (name, inversion, midi) in enumerate(st.session_state.options):
                with cols[i]:
                    draw_keyboard(midi)
                    if st.button(f"Select Option {i+1}", key=f"opt{i}"):
                        if (name, inversion, midi) == q:
                            st.session_state.feedback = "✅ Correct!"
                        else:
                            st.session_state.feedback = f"❌ Wrong! Correct: {q[0]} ({q[1]})"
                        st.session_state.question = None

    if st.session_state.feedback:
        st.write(st.session_state.feedback)
