import random
import streamlit as st

# Define chords
chords = {
    "C major": ["C", "E", "G"],
    "D minor": ["D", "F", "A"],
    "E minor": ["E", "G", "B"],
    "F major": ["F", "A", "C"],
    "G major": ["G", "B", "D"],
    "A minor": ["A", "C", "E"],
    "B diminished": ["B", "D", "F"]
}

# Generate a random chord and inversion
def generate_chord():
    chord_name, notes = random.choice(list(chords.items()))
    inversion = random.choice([0, 1, 2])  # 0 = root, 1st, 2nd
    inverted = notes[inversion:] + notes[:inversion]
    return chord_name, inversion, inverted

# App
st.title("🎹 Chord Trainer")

if "chord" not in st.session_state:
    st.session_state.chord = generate_chord()

chord_name, inversion, notes = st.session_state.chord
st.write(f"Notes: {', '.join(notes)}")

# Dropdown answer
inv_map = {0: "root position", 1: "1st inversion", 2: "2nd inversion"}
options = [f"{name} {pos}" for name in chords.keys() for pos in inv_map.values()]
answer = st.selectbox("Select your answer:", options)

if st.button("Check"):
    correct = f"{chord_name} {inv_map[inversion]}"
    if answer == correct:
        st.success("✅ Correct!")
    else:
        st.error(f"❌ Wrong. Correct answer: {correct}")
    # Generate new chord
    st.session_state.chord = generate_chord()
