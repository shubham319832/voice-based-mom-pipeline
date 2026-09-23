import os
from pathlib import Path

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
# AI IMPORTS
# ============================================================

from faster_whisper import WhisperModel
from pyannote.audio import Pipeline

# IMPORTANT:
# All project modules are inside the src package.
from src.audio_utils import convert_to_wav
from src.align import align_transcript
from src.stats import calculate_speaker_statistics
from src.meeting_analysis import analyze_meeting
from src.save_results import save_results


# ============================================================
# CONFIGURATION
# ============================================================

WHISPER_MODEL = "small"


# ============================================================
# LOAD WHISPER MODEL
# ============================================================

def load_whisper_model():

    print("Loading Whisper model...")

    model = WhisperModel(
        WHISPER_MODEL,
        device="cuda",
        compute_type="float16"
    )

    print("Whisper model loaded successfully!")

    return model


# ============================================================
# LOAD DIARIZATION MODEL
# ============================================================

def load_diarization_model():

    print("Loading speaker diarization model...")

    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-community-1"
    )

    print("Diarization model loaded successfully!")

    return pipeline


# ============================================================
# MAIN MEETING PROCESSING FUNCTION
# ============================================================

def process_meeting(
    input_file,
    output_audio="data/audio/meeting_audio.wav"
):

    input_file = Path(input_file)
    output_audio = Path(output_audio)

    # Make sure output directory exists
    output_audio.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # ========================================================
    # STEP 1: AUDIO PREPROCESSING
    # ========================================================

    print("\n==============================")
    print("STEP 1: AUDIO PREPROCESSING")
    print("==============================")

    convert_to_wav(
        input_file=input_file,
        output_file=output_audio
    )

    print("Audio preprocessing completed!")

    # ========================================================
    # STEP 2: TRANSCRIPTION
    # ========================================================

    print("\n==============================")
    print("STEP 2: TRANSCRIPTION")
    print("==============================")

    whisper_model = load_whisper_model()

    segments, info = whisper_model.transcribe(
        str(output_audio),
        beam_size=5
    )

    transcript_segments = []

    for segment in segments:

        transcript_segments.append(
            {
                "start": round(
                    segment.start,
                    2
                ),
                "end": round(
                    segment.end,
                    2
                ),
                "text": segment.text.strip()
            }
        )

    print("Transcription completed!")

    print(
        "Detected language:",
        info.language
    )

    print(
        "Language probability:",
        info.language_probability
    )

    # ========================================================
    # STEP 3: SPEAKER DIARIZATION
    # ========================================================

    print("\n==============================")
    print("STEP 3: SPEAKER DIARIZATION")
    print("==============================")

    diarization_pipeline = (
        load_diarization_model()
    )

    diarization_output = (
        diarization_pipeline(
            str(output_audio)
        )
    )

    speaker_segments = []

    for turn, speaker in (
        diarization_output.speaker_diarization
    ):

        speaker_segments.append(
            {
                "start": turn.start,
                "end": turn.end,
                "speaker": speaker
            }
        )

    print(
        "Speaker diarization completed!"
    )

    # ========================================================
    # STEP 4: ALIGN SPEAKERS WITH TRANSCRIPT
    # ========================================================

    print("\n==============================")
    print("STEP 4: SPEAKER ALIGNMENT")
    print("==============================")

    aligned_segments = align_transcript(
        transcript_segments,
        speaker_segments
    )

    print(
        "Speaker alignment completed!"
    )

    # ========================================================
    # STEP 5: SPEAKER STATISTICS
    # ========================================================

    print("\n==============================")
    print("STEP 5: SPEAKER STATISTICS")
    print("==============================")

    speaker_statistics = (
        calculate_speaker_statistics(
            aligned_segments
        )
    )

    print(
        "Speaker statistics calculated!"
    )

    # ========================================================
    # STEP 6: MEETING ANALYSIS
    # ========================================================

    print("\n==============================")
    print("STEP 6: MEETING ANALYSIS")
    print("==============================")

    meeting_analysis = analyze_meeting(
        aligned_segments
    )

    print(
        "Meeting analysis completed!"
    )

    # ========================================================
    # STEP 7: SAVE JSON RESULT
    # ========================================================

    print("\n==============================")
    print("STEP 7: SAVING RESULT")
    print("==============================")

    result_file = save_results(
        transcript=aligned_segments,
        speaker_statistics=speaker_statistics,
        language=info.language,
        language_probability=(
            info.language_probability
        ),
        meeting_analysis=meeting_analysis
    )

    print(
        "\nComplete meeting processing finished!"
    )

    # ========================================================
    # RETURN STRUCTURED RESULT
    # ========================================================

    return {
        "language": info.language,

        "language_probability": (
            info.language_probability
        ),

        "transcript": aligned_segments,

        "speaker_statistics": speaker_statistics,

        "meeting_analysis": meeting_analysis,

        "result_file": str(result_file)
    }