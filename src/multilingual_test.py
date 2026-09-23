import os

# CUDA DLL paths
os.add_dll_directory(
    r"C:\Users\shubh\Pycharmvoice-mom-ai\.venv\Lib\site-packages\nvidia\cublas\bin"
)
os.add_dll_directory(
    r"C:\Users\shubh\Pycharmvoice-mom-ai\.venv\Lib\site-packages\nvidia\cudnn\bin"
)

from faster_whisper import WhisperModel

AUDIO_FILE = "data/uploads/test_60sec.wav"

print("\n==============================")
print("LOADING WHISPER")
print("==============================")

model = WhisperModel(
    "small",
    device="cuda",
    compute_type="float16"
)

print("Whisper loaded successfully!")

print("\n==============================")
print("MULTILINGUAL TEST")
print("==============================")

segments, info = model.transcribe(
    AUDIO_FILE,
    beam_size=5
)

print("Detected language:", info.language)
print("Language probability:", info.language_probability)

print("\nTRANSCRIPT:")
print("------------------------------")

for segment in segments:
    print(
        f"[{segment.start:.2f}s - {segment.end:.2f}s] "
        f"{segment.text.strip()}"
    )

print("\n==============================")
print("MULTILINGUAL TEST COMPLETE")
print("==============================")