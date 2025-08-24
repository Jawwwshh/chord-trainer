import streamlit as st
import matplotlib.pyplot as plt
import random

# 🎹 Define 25-key keyboard (C3–C5)
WHITE_KEYS = ["C", "D", "E", "F", "G", "A", "B"]
BLACK_KEYS = ["C#", "D#", "F#", "G#", "A#"]
START_OCTAVE = 3
NUM_KEYS = 25  # C3 → C5

# Build full note list
NOTES = []
for i in range(NUM_KEYS):
    octave = START_OCTAVE + (i // 12)
    note_name = WHITE_KEYS[i % 7] if (i % 12) in [0,2,4,5,7,9,11] else None
    # Actually define by semitones
    SEMI_TO_NOTE = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
    note = SEMI_TO_NOTE[i % 12] + str(START_OCTAVE + (i // 12))
    NOTES.append(note)

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

SEMI_TO_NOTE = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
NOTE_TO_SEMI = {n: i for i, n in enumerate(SEMI_TO_NOTE)}

def note_name_to_midi(note):
    name, octave = note[:-1], int(note[-1])
    return NOTE_TO_SEMI[name] + 12 * octave

def midi_to_note_name(midi):
    octave = midi // 12
    name = SEMI_TO_NOTE[midi % 12]
    return f"{name}{octave}"

def build_chord(root, quality, inversion="root", octave=4):
    """Return chord note list given root, quality, and inversion, centered in keyboard range"""
    base_midi = NOTE_TO_SEMI[root] + 12 * octave
    intervals = CHORD_STRUCTURES[quality]
    notes = [base_midi + i for i in intervals]

    # Apply inversion
    inv_order = INVERSIONS[inversion]
    notes = [notes[i] for i in inv_order]
    for j in range(inv_order[0]):
        notes[j] += 12

    # Center chord inside 25-key window (C3–C5)
    lowest = min(notes)
    highest = max(notes)
    mid = (lowest + highest) // 2
    center_target = note_name_to_midi("C4")  # aim near middle C
    shift = (center_target - mid)
    notes = [n + shift for n in notes]

    return [midi_to_note_name(n) for n in notes]

def draw_keyboard(highlight_notes):
    fig, ax = plt.subplots(figsize=(10, 2))
    white_key_width = 1
    white_key_height = 4
    black_key_width = 0.6
    black_key_height = 2.5

    highlight_set = set(highlight_notes)

    # Track where each white key lands (for black placement)
    white_positions = []
    x_pos = 0
    for midi in range(note_name_to_midi("C3"), note_name_to_midi("C5") + 1):
        note = midi_to_note_name(midi)
        if note[:-1] in WHITE_KEYS:
            # White key
            color = "yellow" if note in highlight_set else "white"
            ax.add_patch(plt.Rectangle((x_pos, 0), white_key_width, white_key_height,
                                       facecolor=color, edgecolor="black", zorder=1))
            white_positions.append((note, x_pos))
            x_pos += 1

    # Draw black keys relative to their white neighbors
    black_neighbors = {"C": 0, "D": 1, "F": 3, "G": 4, "A": 5}  # position in scale
    for i, (note, x) in enumerate(white_positions):
        base = note[:-1]
        octave = int(note[-1])
        if base in black_neighbors:
            black_note = base + "#" + str(octave)
            if black_note in NOTES:  # inside keyboard range
                bx = x + 0.75  # centered between two white keys
                color = "red" if black_note in highlight_set else "black"
                ax.add_patch(plt.Rectangle((bx - black_key_width/2, white_key_height - black_key_height),
                                           black_key_width, black_key_height,
                                           facecolor=color, edgecolor="black", zorder=2))

    ax.set_xlim(0, x_pos)
    ax.set_ylim(0, white_key_height)
    ax.axis("off")
    return fig

# ---------------- Streamlit App ----------------
st.title("🎹 Chord Trainer")

mode = st.sidebar.radio("Choose Mode", ["Name the Shape", "Identify the Shape"])

active_keys = st.sidebar.multiselect("Select Keys", list(KEYS.keys()), default=["C major","A minor","G major","E minor"])

if st.button("New Question"):
    if active_keys:
        chosen_key = random.choice(active_keys)
        scale = KEYS[chosen_key]
        quality = random.choice(["major","minor"])
        root = random.choice(scale)
        inversion = random.choice(list(INVERSIONS.keys()))

        correct_chord = build_chord(root, quality, inversion)
        correct_label = f"{root} {quality} ({inversion})"

        if mode == "Name the Shape":
            st.write("**Which chord is this?**")
            fig = draw_keyboard(correct_chord)
            st.pyplot(fig)

            guess = st.text_input("Your Answer (e.g. C major (root))")
            if guess:
                if guess.strip().lower() == correct_label.lower():
                    st.success("✅ Correct!")
                else:
                    st.error(f"❌ Wrong. It was {correct_label}")

        elif mode == "Identify the Shape":
            st.write("**Which diagram matches the chord below?**")
            st.write(f"Chord: {correct_label}")

            # generate 3 wrong answers
            options = [(correct_chord, True)]
            while len(options) < 4:
                wrong_key = random.choice(active_keys)
                wrong_scale = KEYS[wrong_key]
                wrong_quality = random.choice(["major","minor"])
                wrong_root = random.choice(wrong_scale)
                wrong_inversion = random.choice(list(INVERSIONS.keys()))
                wrong_chord = build_chord(wrong_root, wrong_quality, wrong_inversion)
                if wrong_chord != correct_chord:
                    options.append((wrong_chord, False))

            random.shuffle(options)

            # display options
            cols = st.columns(2)
            for i, (chord, is_correct) in enumerate(options):
                with cols[i%2]:
                    fig = draw_keyboard(chord)
                    st.pyplot(fig)
                    if st.button(f"Select Option {i+1}", key=f"opt{i}"):
                        if is_correct:
                            st.success("✅ Correct!")
                        else:
                            st.error("❌ Wrong!")
