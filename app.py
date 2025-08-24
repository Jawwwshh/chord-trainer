import streamlit as st
import matplotlib.pyplot as plt
import random

# 🎹 Define 25-key keyboard (C3–C5)
START_NOTE = 48  # MIDI for C3
NUM_KEYS = 25   # C3 → C5

SEMI_TO_NOTE = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
NOTE_TO_SEMI = {n: i for i, n in enumerate(SEMI_TO_NOTE)}

# 🎶 Chord definitions relative to root
CHORD_STRUCTURES = {
    "major": [0, 4, 7],
    "minor": [0, 3, 7]
}

INVERSIONS = {
    "root": [0, 1, 2],
    "1st": [1, 2, 0],
    "2nd": [2, 0, 1],
}

# Keys to work with
KEYS = {
    "C major": ["C", "D", "E", "F", "G", "A", "B"],
    "A minor": ["A", "B", "C", "D", "E", "F", "G"],
    "G major": ["G", "A", "B", "C", "D", "E", "F#"],
    "E minor": ["E", "F#", "G", "A", "B", "C", "D"],
}

def note_name_to_midi(note):
    name, octave = note[:-1], int(note[-1])
    return NOTE_TO_SEMI[name] + 12 * octave

def midi_to_note_name(midi):
    octave = midi // 12
    name = SEMI_TO_NOTE[midi % 12]
    return f"{name}{octave}"

def build_chord(root, quality, inversion="root", octave=4):
    """Return chord as MIDI numbers, centered in 25-key window"""
    base_midi = NOTE_TO_SEMI[root] + 12 * octave
    intervals = CHORD_STRUCTURES[quality]
    notes = [base_midi + i for i in intervals]

    # Apply inversion
    inv_order = INVERSIONS[inversion]
    notes = [notes[i] for i in inv_order]
    for j in range(inv_order[0]):
        notes[j] += 12

    # Center chord inside 25-key window
    lowest, highest = min(notes), max(notes)
    mid = (lowest + highest) // 2
    center_target = note_name_to_midi("C4")
    shift = (center_target - mid)
    notes = [n + shift for n in notes]

    return notes  # MIDI numbers

def draw_keyboard(highlight_midis, width=25):
    fig, ax = plt.subplots(figsize=(8, 2))
    start_note = START_NOTE
    end_note = start_note + width - 1

    white_keys = [0, 2, 4, 5, 7, 9, 11]
    black_keys = [1, 3, 6, 8, 10]

    white_index = 0
    for midi in range(start_note, end_note+1):
        x = white_index
        if midi % 12 in white_keys:
            rect = plt.Rectangle((x, 0), 1, 1, facecolor="white", edgecolor="black")
            ax.add_patch(rect)
            if midi in highlight_midis:
                ax.add_patch(plt.Rectangle((x, 0), 1, 1, facecolor="yellow", alpha=0.5))
            white_index += 1

    white_index = 0
    for midi in range(start_note, end_note+1):
        if midi % 12 in white_keys:
            x = white_index
            white_index += 1
        if midi % 12 in black_keys:
            rect = plt.Rectangle((x-0.3, 0.5), 0.6, 0.5, facecolor="black", edgecolor="black", zorder=2)
            ax.add_patch(rect)
            if midi in highlight_midis:
                ax.add_patch(plt.Rectangle((x-0.3, 0.5), 0.6, 0.5, facecolor="red", alpha=0.5, zorder=3))

    ax.set_xlim(0, white_index)
    ax.set_ylim(0, 1)
    ax.axis("off")
    st.pyplot(fig)

# ---------------- Streamlit App ----------------
st.title("🎹 Chord Trainer")

mode = st.sidebar.radio("Choose Mode", ["Name the Shape", "Identify the Shape"])
active_keys = st.sidebar.multiselect("Select Keys", list(KEYS.keys()), default=list(KEYS.keys()))

if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = None
    st.session_state.feedback = ""

if st.button("New Question"):
    chosen_key = random.choice(active_keys)
    scale = KEYS[chosen_key]
    quality = random.choice(["major", "minor"])
    root = random.choice(scale)
    inversion = random.choice(list(INVERSIONS.keys()))

    correct_chord = build_chord(root, quality, inversion)
    correct_label = f"{root} {quality} ({inversion})"

    options = [(correct_chord, True)]
    while len(options) < 4:
        wrong_key = random.choice(active_keys)
        wrong_scale = KEYS[wrong_key]
        wrong_quality = random.choice(["major", "minor"])
        wrong_root = random.choice(wrong_scale)
        wrong_inversion = random.choice(list(INVERSIONS.keys()))
        wrong_chord = build_chord(wrong_root, wrong_quality, wrong_inversion)
        if wrong_chord != correct_chord:
            options.append((wrong_chord, False))
    random.shuffle(options)

    st.session_state.quiz_data = {
        "mode": mode,
        "correct_label": correct_label,
        "options": options
    }
    st.session_state.feedback = ""

if st.session_state.quiz_data:
    mode = st.session_state.quiz_data["mode"]
    correct_label = st.session_state.quiz_data["correct_label"]

    if mode == "Name the Shape":
        st.write("**Which chord is this?**")
        draw_keyboard(st.session_state.quiz_data["options"][0][0])
        guess = st.text_input("Your Answer (e.g. C major (root))")
        if guess:
            if guess.strip().lower() == correct_label.lower():
                st.success("✅ Correct!")
            else:
                st.error(f"❌ Wrong. It was {correct_label}")

    elif mode == "Identify the Shape":
        st.write("**Which diagram matches the chord below?**")
        st.write(f"Chord: {correct_label}")

        cols = st.columns(2)
        for i, (chord, is_correct) in enumerate(st.session_state.quiz_data["options"]):
            with cols[i % 2]:
                draw_keyboard(chord)
                if st.button(f"Select Option {i+1}", key=f"opt{i}"):
                    if is_correct:
                        st.session_state.feedback = "✅ Correct!"
                    else:
                        st.session_state.feedback = f"❌ Wrong! It was {correct_label}"
                    st.session_state.quiz_data = None

    if st.session_state.feedback:
        st.write(st.session_state.feedback)
