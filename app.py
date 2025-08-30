import streamlit as st
import random
from collections import defaultdict
from PIL import Image, ImageDraw

# --- Import chord data from external files ---
from Chords.chords import CHORDS
from Chords.voicings import CHORD_VOICINGS

# --- Function to reset session state ---
def reset_session_state_for_mode(mode_to_keep):
    """Reset session state keys for the mode not currently selected."""
    # Keys for identify the position
    identify_keys = ["current_chord", "attempts", "show_result", "last_attempt"]
    # Keys for playing the position
    play_keys = ["play_current_chord", "play_feedback", "play_clicked_option", "play_options"]

    if mode_to_keep == "identify the position":
        for key in play_keys:
            if key in st.session_state:
                del st.session_state[key]
    elif mode_to_keep == "Playing the Position":
        for key in identify_keys:
            if key in st.session_state:
                del st.session_state[key]


# --- MODE SELECTION (top of page) ---
mode = st.sidebar.selectbox("Select Mode", ["identify the position", "Playing the Position"])
reset_session_state_for_mode(mode)

# --- MOBILE-FRIENDLY BUTTONS CSS ---
st.markdown("""
<style>
@media (max-width: 600px) {
    div.stButton > button {
        padding: 4px 8px;
        font-size: 12px;
        margin-bottom: 4px;
    }
}
</style>
""", unsafe_allow_html=True)

# --- Group chords by base name ---
grouped_chords = defaultdict(list)
for chord_name in CHORDS.keys():
    words = chord_name.split()
    if "major" in words or "minor" in words or "diminished" in words:
        if "seventh" in chord_name or "flat five" in chord_name or "dominant" in chord_name:
            base = " ".join(words[:3])
        else:
            base = " ".join(words[:2])
    else:
        base = " ".join(words[:2])
    grouped_chords[base].append(chord_name)

# --- Sidebar selection ---
st.sidebar.title("Select Chords for Quiz")
selected_base_chords = []

categories = {"Major": [], "Minor": [], "Diminished": [], "Sevenths & Extensions": []}

for base in grouped_chords.keys():
    if "major" in base and "seventh" not in base:
        categories["Major"].append(base)
    elif "minor" in base and "seventh" not in base:
        categories["Minor"].append(base)
    elif "diminished" in base:
        categories["Diminished"].append(base)
    else:
        categories["Sevenths & Extensions"].append(base)

for cat in categories:
    categories[cat].sort()

for cat, bases in categories.items():
    with st.sidebar.expander(cat, expanded=True):
        for base in bases:
            if st.checkbox(base, value=base in ["C major", "A minor", "E minor", "G major"]):
                selected_base_chords.append(base)

if not selected_base_chords:
    st.warning("Please select at least one chord.")
    st.stop()

# --- Build selected chords dict ---
selected_chords_dict = {base: grouped_chords[base] for base in selected_base_chords}
all_selected_chords = [ch for sublist in selected_chords_dict.values() for ch in sublist]

# ---------------------------
# IDENTIFY THE POSITION MODE
# ---------------------------
if mode == "identify the position":
    # --- Initialize session state ---
    if "current_chord" not in st.session_state or st.session_state.current_chord not in all_selected_chords:
        st.session_state.current_chord = random.choice(all_selected_chords)
    if "attempts" not in st.session_state:
        st.session_state.attempts = {}
    if "show_result" not in st.session_state:
        st.session_state.show_result = False
    if "last_attempt" not in st.session_state:
        st.session_state.last_attempt = None

    # --- Next chord ---
    if st.button("Next Chord", key="next_chord_position"):
        remaining_chords = [ch for ch in all_selected_chords if ch != st.session_state.current_chord]
        if remaining_chords:
            st.session_state.current_chord = random.choice(remaining_chords)
        st.session_state.attempts[st.session_state.current_chord] = []
        st.session_state.show_result = False
        st.session_state.last_attempt = None

    chord_key = st.session_state.current_chord
    st.write(f"### Notes: {', '.join(CHORDS[chord_key])}")

    # --- Handle button clicks ---
    def handle_option(option):
        clicked = st.button(option, key=f"{chord_key}_{option}")
        if clicked:
            if chord_key not in st.session_state.attempts:
                st.session_state.attempts[chord_key] = []
            if option not in st.session_state.attempts[chord_key]:
                st.session_state.attempts[chord_key].append(option)
            st.session_state.show_result = True
            st.session_state.last_attempt = option
        return clicked

    # --- Display columns of options with feedback ---
    sorted_bases = sorted(selected_base_chords)
    cols = st.columns(len(sorted_bases))

    for col_idx, base in enumerate(sorted_bases):
        with cols[col_idx]:
            st.write(f"**{base}**")
            options = selected_chords_dict[base]

            # Root chord first
            root_options = [opt for opt in options if "root" in opt.lower()]
            other_options = [opt for opt in options if "root" not in opt.lower()]
            options_sorted = root_options + sorted(other_options)

            for option in options_sorted:
                handle_option(option)

                # Feedback coloring for attempted options
                attempts = st.session_state.attempts.get(chord_key, [])
                if option in attempts:
                    if option == chord_key:
                        st.success(f"{option} ✅")
                    else:
                        st.error(f"{option} ❌")

    # --- Display bottom feedback ---
    attempts = st.session_state.attempts.get(chord_key, [])
    if attempts and st.session_state.last_attempt:
        if st.session_state.last_attempt == chord_key:
            st.success(f"✅ Correct! It was {chord_key}")
        else:
            st.error(f"❌ Incorrect. Try again!")

# ---------------------------
# PLAYING THE POSITION MODE
# ---------------------------
elif mode == "Playing the Position":
    # --- Generate keyboard images ---
    def generate_keyboard_image(highlight_notes, low_note="C3", high_note="C6"):
        import re

        key_order = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
        naturals_to_index = {"C":0,"D":2,"E":4,"F":5,"G":7,"A":9,"B":11}

        def to_sharp(note_with_octave: str) -> str:
            m = re.match(r"^([A-Ga-g])([#b]?)(\d)$", note_with_octave.strip())
            if not m:
                return note_with_octave.strip()
            letter = m.group(1).upper()
            accidental = m.group(2)
            octave = int(m.group(3))

            semitone = naturals_to_index[letter]
            if accidental == "#":
                semitone += 1
            elif accidental == "b":
                semitone -= 1

            if semitone >= 12:
                semitone -= 12
                octave += 1
            elif semitone < 0:
                semitone += 12
                octave -= 1

            return f"{key_order[semitone]}{octave}"

        highlight_sharp = {to_sharp(n) for n in highlight_notes}

        def split_note(n):
            return n[:-1], int(n[-1])
        low_pc, low_oct = split_note(low_note)
        high_pc, high_oct = split_note(high_note)

        keyboard_notes = []
        for octave in range(low_oct, high_oct + 1):
            for pc in key_order:
                full = f"{pc}{octave}"
                keyboard_notes.append(full)
                if full == high_note:
                    break
            if keyboard_notes[-1] == high_note:
                break

        img_width, img_height = 700, 150
        white_key_height = img_height
        black_key_height = int(img_height * 0.6)

        white_keys = [n for n in keyboard_notes if "#" not in n]
        white_key_width = img_width / len(white_keys)

        img = Image.new("RGB", (img_width, img_height), "white")
        draw = ImageDraw.Draw(img)

        white_key_positions = {}
        x = 0
        for note in keyboard_notes:
            if "#" not in note:
                fill = "yellow" if note in highlight_sharp else "white"
                draw.rectangle([x, 0, x + white_key_width, white_key_height], fill=fill, outline="black")
                white_key_positions[note] = x
                x += white_key_width

        for idx, note in enumerate(keyboard_notes):
            if "#" in note:
                left_idx = idx - 1
                if keyboard_notes[left_idx] in white_key_positions:
                    x0 = white_key_positions[keyboard_notes[left_idx]] + white_key_width * 0.65
                    x1 = x0 + white_key_width * 0.7
                    fill = "yellow" if note in highlight_sharp else "black"
                    draw.rectangle([x0, 0, x1, black_key_height], fill=fill, outline="black")

        return img

    available_chords = [ch for ch in all_selected_chords if ch in CHORD_VOICINGS]
    if not available_chords:
        st.warning("None of your selected chords have voicings in the database. Paste your lines into RAW_VOICINGS using the exact chord names.")
        st.stop()

    # --- Initialize session state ---
    if "play_current_chord" not in st.session_state:
        st.session_state.play_current_chord = random.choice(available_chords)
        st.session_state.play_feedback = ""
        st.session_state.play_clicked_option = None
    if "play_options" not in st.session_state:
        st.session_state.play_options = None

    if st.button("Next Chord", key="next_chord_play"):
        pool = [ch for ch in available_chords if ch != st.session_state.play_current_chord] or available_chords
        st.session_state.play_current_chord = random.choice(pool)
        st.session_state.play_feedback = ""
        st.session_state.play_clicked_option = None
        st.session_state.play_options = None

    current_chord = st.session_state.play_current_chord
    st.write(f"### Which diagram shows: {current_chord}?")

    if st.session_state.play_options is None:
        correct_notes = CHORD_VOICINGS[current_chord]
        correct_img = generate_keyboard_image(correct_notes)

        other_chords = [ch for ch in available_chords if ch != current_chord]
        wrong_chords = random.sample(other_chords, min(3, len(other_chords)))
        wrong_imgs = [generate_keyboard_image(CHORD_VOICINGS[ch]) for ch in wrong_chords]

        options = [(current_chord, correct_img)] + list(zip(wrong_chords, wrong_imgs))
        random.shuffle(options)
        st.session_state.play_options = options

    # --- Display clickable images as buttons ---
    cols = st.columns(len(st.session_state.play_options))
    for idx, (chord_name, img) in enumerate(st.session_state.play_options):
        with cols[idx]:
            # Clickable button with image as content
            clicked = st.button("", key=f"play_{chord_name}", help="Click the image")
            st.image(img, use_container_width=True)  # fixed deprecated parameter
            if clicked:
                st.session_state.play_clicked_option = chord_name
                if chord_name == current_chord:
                    st.session_state.play_feedback = f"✅ Correct! It was {current_chord}"
                else:
                    st.session_state.play_feedback = f"❌ Incorrect, that was {chord_name}. Try again!"

    # --- Show feedback ---
    if st.session_state.play_feedback:
        st.info(st.session_state.play_feedback)
