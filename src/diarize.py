from pyannote.audio import Pipeline

AUDIO_FILE = "data/uploads/test_60sec.wav"

print("Loading speaker diarization model...")

pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-community-1"
)

print("Model loaded successfully!")
print("Starting speaker diarization...")
print(f"Input file: {AUDIO_FILE}")

output = pipeline(AUDIO_FILE)

print("\n===== SPEAKER DIARIZATION =====")

for turn, speaker in output.speaker_diarization:
    print(
        f"[{turn.start:.2f}s - {turn.end:.2f}s] "
        f"{speaker}"
    )

print("\n===== DIARIZATION COMPLETE =====")