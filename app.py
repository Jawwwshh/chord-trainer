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
# MIDI helper
# -------------------
SEMI_TO_NOTE = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
NOTE_TO_SEMI = {n:i for i,n in enumerate(SEMI_TO_NOTE)}

def note_name_to_midi(note_name, octave):
    return NOTE_TO_SEMI[note_name] + 12 * octave

# -------------------
# Build chord MIDI notes
# -------------------
def build_chord_midi(chord_name, inversion, base_octave=4):
    intervals = CHORDS[chord_name]  # e.g., [0,4,7]
    root_note = chord_name.split()[0]
    root_midi = note_name_to_midi(root_note, base_octave)

    # Base notes
    notes = [root_midi + i for i in intervals]

    # Apply inversion
    order = INVERSIONS[inversion]
    notes = [notes[i] for i in order]

    return notes

# -------------------
# Draw keyboard
# -------------------
def draw_keyboard(chord_midis, start_note="C3", end_note="C5"):
    start_midi = note_name_to_midi(start_note[:-1], int(start_note[-1]))
    end_midi = note_name_to_midi(end_note[:-1], int(end_note[-1]))

    WHITE_SEMITONES = {0,2,4,5,7,9,11}  # C D E F G A B
    BLACK_AFTER_WHITE = {0,2,5,7,9}     # C D F G A

    # Map white keys to x positions
    white_order = []
    white_x_map = {}
    x = 0
    for m in range(start_midi, end_midi+1):
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

    # Draw black keys
    for m in white_order:
        if m % 12 in BLACK_AFTER_WHITE:
            b = m + 1
            if start_midi <= b <= end_midi:
                wx = white_x_map[m]
                bx = wx + 1 - black_w/2
                face = "red" if b in chord_set else "black"
                ax.add_patch(plt.Rectangle((bx, white_h - black_h), black_w, black_h, facecolor=face, edgecolor="black", zorder=2))

    ax.set_xlim(0, len(white_order))
    ax.set_ylim(0, white_h)
    ax.axis("off")
    st.pyplot(fig)

# -------------------
# Generate question
# -------------------
def generate_question(selected_chords):
    chord_name = random.choice(selected_chords)
    inversion = random.choice(list(INVERSIONS.keys()))
    midi_notes = build_chord_midi(chord_name, inversion, base_octave=4)
    return {"chord_name": chord_name, "inversion": inversion, "midi_notes": midi_notes}

# -------------------
# Streamlit App
# -------------------
st.title("🎹 Chord Trainer")

selected_chords = st.multiselect(
    "Select chords to practice", 
    list(CHORDS.keys()), 
    default=list(CHORDS.keys())
)

mode = st.radio("Mode", ["Name → Picture", "Picture → Name"])

if "question" not in st.session_state:
    st.session_state.question = None
    st.session_state.options = []
    st.session_state.feedback = ""

if st.button("Next Question") or st.session_state.question is None:
    st.session_state.question = generate_question(selected_chords)

    # Build options for "Picture → Name"
    if mode == "Picture → Name":
        correct = st.session_state.question
        options = [correct]
        while len(options) < 4:
            wrong = generate_question(selected_chords)
            if wrong not in options:
                options.append(wrong)
        random.shuffle(options)
        st.session_state.options = options
    st.session_state.feedback = ""

# -------------------
# Display question
# -------------------
q = st.session_state.question

if mode == "Name → Picture":
    st.write(f"Which diagram shows **{q['chord_name']} ({q['inversion']})**?")
    draw_keyboard(q['midi_notes'])

elif mode == "Picture → Name":
    st.write("Which diagram matches the chord shown?")
    cols = st.columns(2)
    for i, option in enumerate(st.session_state.options):
        with cols[i % 2]:
            draw_keyboard(option['midi_notes'])
            if st.button(f"Select Option {i+1}", key=f"opt{i}"):
                if option == q:
                    st.session_state.feedback = "✅ Correct!"
                else:
                    st.session_state.feedback = f"❌ Wrong! Correct: {q['chord_name']} ({q['inversion']})"
                st.session_state.question = None  # clear to generate new question next click

if st.session_state.feedback:
    st.write(st.session_state.feedback)

