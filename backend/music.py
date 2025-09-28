import os
from google import genai
from google.genai import types
from mido import Message, MidiFile, MidiTrack, bpm2tempo, MetaMessage
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Missing GEMINI_API_KEY in .env")

client = genai.Client(api_key=api_key)

# Ask Gemini to expand a seed into a melody
seed = "C4 (1), D4 (1), E4 (1), F4 (1), G4 (2), E4 (2)"
style = "very rapidly fast paced, simple melody "
prompt = """
You are a composer. Given a seed melody, extend it into a 16-bar song, allowing multiple notes at once (polyphony, i.e., chords or harmonies).
Give the piece an Ancient Greek music vibe (use Greek modes, tempo, ornamentation, and phrasing).
Output strictly in JSON with keys: tempo, key, and notes[],
where each note is either a single pitch (like C4, D#3) or a list of pitches (for chords, e.g., ["C4", "E4", "G4, "Bb5"]). Each note/chord has a duration in beats.
Example:
{
    "tempo": 90,
    "key": "D Dorian",
    "notes": [
        {"pitch": "C4", "duration": 1},
        {"pitch": ["E4", "G4"], "duration": 2}
    ]
}
Make sure to add no comments or other weird structures, just valid JSON.

seed melody:
""" + seed + "\nstyle: " + style

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
)

# Parse JSON text from Gemini
import json
try:
    music_data = json.loads(response.text.replace('```json', '').strip('`'))
except Exception:
    raise ValueError("Gemini output was not valid JSON:\n" + response.text)

print("Generated music plan:", music_data)

from mido import Message, MidiFile, MidiTrack, bpm2tempo



def note_to_midi(pitch: str) -> int:
    """Convert pitch name like C4, C#4, Bb10 to MIDI number."""
    note_names = {'C':0,'C#':1,'Db':1,'D':2,'D#':3,'Eb':3,'E':4,'F':5,
                  'F#':6,'Gb':6,'G':7,'G#':8,'Ab':8,'A':9,'A#':10,'Bb':10,'B':11}
    # Find where the octave number starts (first digit)
    for i, c in enumerate(pitch):
        if c.isdigit():
            name = pitch[:i]
            octave = int(pitch[i:])
            break
    else:
        raise ValueError(f"Invalid pitch format: {pitch}")
    return 12 * (octave + 1) + note_names[name]

def make_midi(music_data, filename="output.mid"):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    tempo = bpm2tempo(music_data.get("tempo", 120))
    track.append(Message('program_change', program=73, time=0))  # Flute
    track.append(MetaMessage('set_tempo', tempo=tempo, time=0))

    ticks_per_beat = mid.ticks_per_beat

    for note in music_data["notes"]:
        pitches = note["pitch"]
        duration_beats = note["duration"]

        if isinstance(pitches, str):
            pitches = [pitches]  # wrap single note in list

        duration_ticks = int(duration_beats * ticks_per_beat)

        # Note on for all pitches (chord)
        for pitch_str in pitches:
            note_number = note_to_midi(pitch_str)
            track.append(Message('note_on', note=note_number, velocity=64, time=0))

        # Note off for all pitches after duration
        for i, pitch_str in enumerate(pitches):
            note_number = note_to_midi(pitch_str)
            track.append(Message('note_off', note=note_number, velocity=64, time=duration_ticks if i==0 else 0))

    mid.save(filename)
    abs_path = os.path.abspath(filename)
    print(f"MIDI file saved at: {abs_path}")
    return abs_path

make_midi(music_data)