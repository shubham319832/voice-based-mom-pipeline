import os

# CUDA DLL paths
os.add_dll_directory(
    r"C:\Users\shubh\Pycharmvoice-mom-ai\.venv\Lib\site-packages\nvidia\cublas\bin"
)

os.add_dll_directory(
    r"C:\Users\shubh\Pycharmvoice-mom-ai\.venv\Lib\site-packages\nvidia\cudnn\bin"
)

from faster_whisper import WhisperModel


# ==========================================
# CONFIGURATION
# ==========================================

AUDIO_FILE = "data/uploads/test_meeting.mp4.mp4"

MODEL_SIZE = "small"


# ==========================================
# LOAD WHISPER MODEL
# ==========================================

print("Loading Whisper model...")

model = WhisperModel(
    MODEL_SIZE,
    device="cuda",
    compute_type="float16"
)

print("Whisper model loaded successfully!")


# ==========================================
# TRANSCRIBE AUDIO / VIDEO
# ==========================================

print("Transcribing audio...")
print(f"Input file: {AUDIO_FILE}")

segments, info = model.transcribe(
    AUDIO_FILE,
    beam_size=5
)


# ==========================================
# DISPLAY DETECTED LANGUAGE
# ==========================================

print("\n===== LANGUAGE INFORMATION =====")

print("Detected language:", info.language)
print("Language probability:", info.language_probability)


# ==========================================
# DISPLAY TRANSCRIPT
# ==========================================

print("\n===== TRANSCRIPT =====")

for segment in segments:

    start = segment.start
    end = segment.end
    text = segment.text.strip()

    print(
        f"[{start:.2f}s - {end:.2f}s] "
        f"{text}"
    )


# ==========================================
# COMPLETE
# ==========================================

print("\n===== TRANSCRIPTION COMPLETE =====")