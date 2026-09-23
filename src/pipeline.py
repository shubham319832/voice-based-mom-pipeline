import os

# ============================================================
# CUDA DLL PATHS
# ============================================================

os.add_dll_directory(
    r"C:\Users\shubh\Pycharmvoice-mom-ai\.venv\Lib\site-packages\nvidia\cublas\bin"
)

os.add_dll_directory(
    r"C:\Users\shubh\Pycharmvoice-mom-ai\.venv\Lib\site-packages\nvidia\cudnn\bin"
)


# ============================================================
# IMPORTS
# ============================================================

from faster_whisper import WhisperModel
from pyannote.audio import Pipeline

from align import align_transcript
from stats import calculate_speaker_statistics
from meeting_analysis import analyze_meeting
from save_results import save_results


# ============================================================
# CONFIGURATION
# ============================================================

AUDIO_FILE = "data/audio/meeting_audio.wav"
WHISPER_MODEL = "small"


# ============================================================
# STEP 1 — LOAD WHISPER
# ============================================================

print("\n==============================")
print("LOADING WHISPER")
print("==============================")

whisper_model = WhisperModel(
    WHISPER_MODEL,
    device="cuda",
    compute_type="float16"
)

print("Whisper loaded successfully!")


# ============================================================
# STEP 2 — TRANSCRIPTION
# ============================================================

print("\n==============================")
print("STARTING TRANSCRIPTION")
print("==============================")

segments, info = whisper_model.transcribe(
    AUDIO_FILE,
    beam_size=5
)

transcript_segments = []

for segment in segments:

    transcript_segments.append({
        "start": round(segment.start, 2),
        "end": round(segment.end, 2),
        "text": segment.text.strip()
    })


print("Transcription completed!")

print(
    "Detected language:",
    info.language
)

print(
    "Language probability:",
    info.language_probability
)


# ============================================================
# STEP 3 — LOAD DIARIZATION MODEL
# ============================================================

print("\n==============================")
print("LOADING DIARIZATION MODEL")
print("==============================")

diarization_pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-community-1"
)

print("Diarization model loaded!")


# ============================================================
# STEP 4 — SPEAKER DIARIZATION
# ============================================================

print("\n==============================")
print("STARTING SPEAKER DIARIZATION")
print("==============================")

output = diarization_pipeline(
    AUDIO_FILE
)

speaker_segments = []

for turn, speaker in output.speaker_diarization:

    speaker_segments.append({
        "start": turn.start,
        "end": turn.end,
        "speaker": speaker
    })


print("Speaker diarization completed!")


# ============================================================
# STEP 5 — ALIGN TRANSCRIPT WITH SPEAKERS
# ============================================================

print("\n==============================")
print("ALIGNING SPEAKERS + TRANSCRIPT")
print("==============================")

aligned_segments = align_transcript(
    transcript_segments,
    speaker_segments
)

print("Alignment completed!")


# ============================================================
# STEP 6 — DISPLAY FINAL TRANSCRIPT
# ============================================================

print("\n==============================")
print("FINAL SPEAKER TRANSCRIPT")
print("==============================")

for item in aligned_segments:

    print(
        f"[{item['start']:.2f}s - "
        f"{item['end']:.2f}s] "
        f"{item['speaker']}: "
        f"{item['text']}"
    )


# ============================================================
# STEP 7 — CALCULATE SPEAKER STATISTICS
# ============================================================

print("\n==============================")
print("CALCULATING SPEAKER STATISTICS")
print("==============================")

speaker_statistics = calculate_speaker_statistics(
    aligned_segments
)

print("Statistics calculated!")


print("\n==============================")
print("SPEAKER STATISTICS")
print("==============================")

for speaker, statistics in speaker_statistics.items():

    print(f"\n{speaker}")

    print(
        f"Speaking duration: "
        f"{statistics['speaking_duration_seconds']} seconds"
    )

    print(
        f"Segments: "
        f"{statistics['segment_count']}"
    )

    print(
        f"Speaking percentage: "
        f"{statistics['speaking_percentage']}%"
    )


# ============================================================
# STEP 8 — MEETING ANALYSIS
# ============================================================

print("\n==============================")
print("ANALYZING MEETING")
print("==============================")

meeting_analysis = analyze_meeting(
    aligned_segments
)

print("Meeting analysis completed!")


# ============================================================
# DISPLAY SUMMARY
# ============================================================

print("\n==============================")
print("MEETING SUMMARY")
print("==============================")

print(
    meeting_analysis["summary"]
)


# ============================================================
# DISPLAY KEY DISCUSSION POINTS
# ============================================================

print("\n==============================")
print("KEY DISCUSSION POINTS")
print("==============================")

for point in meeting_analysis[
    "key_discussion_points"
]:

    print(
        "-",
        point
    )


# ============================================================
# DISPLAY DECISIONS
# ============================================================

print("\n==============================")
print("DECISIONS")
print("==============================")

for decision in meeting_analysis[
    "decisions"
]:

    print(
        "-",
        decision
    )


# ============================================================
# DISPLAY ACTION ITEMS
# ============================================================

print("\n==============================")
print("ACTION ITEMS")
print("==============================")

for action in meeting_analysis[
    "action_items"
]:

    print(
        f"- {action['speaker']}: "
        f"{action['text']}"
    )


# ============================================================
# STEP 9 — SAVE COMPLETE JSON RESULT
# ============================================================

print("\n==============================")
print("SAVING JSON RESULT")
print("==============================")

save_results(
    transcript=aligned_segments,
    speaker_statistics=speaker_statistics,
    language=info.language,
    language_probability=info.language_probability,
    meeting_analysis=meeting_analysis
)


# ============================================================
# COMPLETE
# ============================================================

print("\n==============================")
print("FULL PIPELINE COMPLETE")
print("==============================")