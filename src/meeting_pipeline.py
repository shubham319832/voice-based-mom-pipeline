import os
from pathlib import Path

# ============================================================
# CUDA DLL PATHS - WINDOWS
# ============================================================

CUDA_DLL_DIRECTORIES = [
    r"C:\Users\shubh\Pycharmvoice-mom-ai\.venv\Lib\site-packages\nvidia\cublas\bin",
    r"C:\Users\shubh\Pycharmvoice-mom-ai\.venv\Lib\site-packages\nvidia\cudnn\bin",
]

for dll_directory in CUDA_DLL_DIRECTORIES:
    if os.path.exists(dll_directory):
        os.add_dll_directory(dll_directory)


# ============================================================
# IMPORTS
# ============================================================

from faster_whisper import WhisperModel
from pyannote.audio import Pipeline

from src.audio_utils import convert_to_wav
from src.align import align_transcript
from src.stats import calculate_speaker_statistics
from src.meeting_analysis import analyze_meeting
from src.save_results import save_results
from src.logger import logger


# ============================================================
# CONFIGURATION
# ============================================================

WHISPER_MODEL = "small"

DIARIZATION_MODEL = (
    "pyannote/speaker-diarization-community-1"
)

AUDIO_OUTPUT = Path(
    "data/audio/meeting_audio.wav"
)


# ============================================================
# LOAD WHISPER MODEL
# ============================================================

def load_whisper_model():

    logger.info(
        "Loading Whisper model: %s",
        WHISPER_MODEL
    )

    print("\n==============================")
    print("LOADING WHISPER MODEL")
    print("==============================")

    model = WhisperModel(
        WHISPER_MODEL,
        device="cuda",
        compute_type="float16"
    )

    logger.info(
        "Whisper model loaded successfully."
    )

    print(
        "Whisper model loaded successfully!"
    )

    return model


# ============================================================
# LOAD DIARIZATION MODEL
# ============================================================

def load_diarization_model():

    logger.info(
        "Loading diarization model: %s",
        DIARIZATION_MODEL
    )

    print("\n==============================")
    print("LOADING DIARIZATION MODEL")
    print("==============================")

    pipeline = Pipeline.from_pretrained(
        DIARIZATION_MODEL
    )

    logger.info(
        "Diarization model loaded successfully."
    )

    print(
        "Diarization model loaded successfully!"
    )

    return pipeline


# ============================================================
# TRANSCRIPTION
# ============================================================

def transcribe_audio(
    model,
    audio_file
):

    logger.info(
        "Starting transcription: %s",
        audio_file
    )

    print("\n==============================")
    print("TRANSCRIPTION")
    print("==============================")

    segments, info = model.transcribe(
        str(audio_file),
        beam_size=5
    )

    transcript_segments = []

    for segment in segments:

        confidence = round(
            segment.avg_logprob,
            4
        )

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
                "text": segment.text.strip(),
                "confidence": confidence
            }
        )

    logger.info(
        "Transcription completed. Language=%s, probability=%.4f, segments=%d",
        info.language,
        info.language_probability,
        len(transcript_segments)
    )

    print(
        f"Detected language: {info.language}"
    )

    print(
        f"Language probability: "
        f"{info.language_probability:.4f}"
    )

    print(
        f"Transcript segments: "
        f"{len(transcript_segments)}"
    )

    return (
        transcript_segments,
        info.language,
        info.language_probability
    )


# ============================================================
# DIARIZATION
# ============================================================

def diarize_audio(
    diarization_pipeline,
    audio_file
):

    logger.info(
        "Starting speaker diarization: %s",
        audio_file
    )

    print("\n==============================")
    print("SPEAKER DIARIZATION")
    print("==============================")

    diarization_output = diarization_pipeline(
        str(audio_file)
    )

    speaker_segments = []

    # pyannote.audio 4.x
    diarization = (
        diarization_output.speaker_diarization
    )

    for turn, speaker in diarization:

        speaker_segments.append(
            {
                "start": round(
                    turn.start,
                    2
                ),
                "end": round(
                    turn.end,
                    2
                ),
                "speaker": speaker
            }
        )

    logger.info(
        "Speaker diarization completed. "
        "Segments=%d",
        len(speaker_segments)
    )

    print(
        f"Speaker segments detected: "
        f"{len(speaker_segments)}"
    )

    for segment in speaker_segments:

        print(
            f"[{segment['start']:.2f}s - "
            f"{segment['end']:.2f}s] "
            f"{segment['speaker']}"
        )

    return speaker_segments


# ============================================================
# COMPLETE PIPELINE
# ============================================================

def process_meeting(
    input_file
):

    input_file = Path(
        input_file
    )

    logger.info(
        "================================================"
    )

    logger.info(
        "Meeting processing started: %s",
        input_file
    )

    print("\n========================================")
    print("VOICE-BASED MINUTES OF MEETING PIPELINE")
    print("========================================")

    try:

        # ----------------------------------------------------
        # INPUT VALIDATION
        # ----------------------------------------------------

        if not input_file.exists():

            logger.error(
                "Input file not found: %s",
                input_file
            )

            raise FileNotFoundError(
                f"Input file not found: {input_file}"
            )

        logger.info(
            "Input file validated successfully."
        )

        # ----------------------------------------------------
        # STEP 1 - AUDIO PREPROCESSING
        # ----------------------------------------------------

        logger.info(
            "Step 1: Audio preprocessing started."
        )

        print("\nSTEP 1: AUDIO PREPROCESSING")

        convert_to_wav(
            input_file,
            AUDIO_OUTPUT
        )

        logger.info(
            "Audio preprocessing completed: %s",
            AUDIO_OUTPUT
        )

        # ----------------------------------------------------
        # STEP 2 - LOAD WHISPER
        # ----------------------------------------------------

        logger.info(
            "Step 2: Loading Whisper."
        )

        print("\nSTEP 2: LOAD WHISPER")

        whisper_model = (
            load_whisper_model()
        )

        # ----------------------------------------------------
        # STEP 3 - TRANSCRIPTION
        # ----------------------------------------------------

        logger.info(
            "Step 3: Transcription."
        )

        print("\nSTEP 3: TRANSCRIPTION")

        (
            transcript_segments,
            language,
            language_probability
        ) = transcribe_audio(
            whisper_model,
            AUDIO_OUTPUT
        )

        # ----------------------------------------------------
        # STEP 4 - LOAD DIARIZATION
        # ----------------------------------------------------

        logger.info(
            "Step 4: Loading diarization."
        )

        print("\nSTEP 4: LOAD DIARIZATION")

        diarization_pipeline = (
            load_diarization_model()
        )

        # ----------------------------------------------------
        # STEP 5 - DIARIZATION
        # ----------------------------------------------------

        logger.info(
            "Step 5: Speaker diarization."
        )

        print(
            "\nSTEP 5: SPEAKER DIARIZATION"
        )

        speaker_segments = (
            diarize_audio(
                diarization_pipeline,
                AUDIO_OUTPUT
            )
        )

        # ----------------------------------------------------
        # STEP 6 - ALIGNMENT
        # ----------------------------------------------------

        logger.info(
            "Step 6: Transcript and speaker alignment."
        )

        print("\nSTEP 6: ALIGNMENT")

        aligned_segments = (
            align_transcript(
                transcript_segments,
                speaker_segments
            )
        )

        logger.info(
            "Alignment completed. Segments=%d",
            len(aligned_segments)
        )

        print(
            f"Aligned transcript segments: "
            f"{len(aligned_segments)}"
        )

        # ----------------------------------------------------
        # STEP 7 - SPEAKER STATISTICS
        # ----------------------------------------------------

        logger.info(
            "Step 7: Calculating speaker statistics."
        )

        print(
            "\nSTEP 7: SPEAKER STATISTICS"
        )

        speaker_statistics = (
            calculate_speaker_statistics(
                aligned_segments
            )
        )

        logger.info(
            "Speaker statistics calculated for %d speakers.",
            len(speaker_statistics)
        )

        # ----------------------------------------------------
        # STEP 8 - MEETING ANALYSIS
        # ----------------------------------------------------

        logger.info(
            "Step 8: Meeting analysis."
        )

        print(
            "\nSTEP 8: MEETING ANALYSIS"
        )

        meeting_analysis = (
            analyze_meeting(
                aligned_segments
            )
        )

        logger.info(
            "Meeting analysis completed."
        )

        # ----------------------------------------------------
        # STEP 9 - SAVE RESULTS
        # ----------------------------------------------------

        logger.info(
            "Step 9: Saving results."
        )

        print(
            "\nSTEP 9: SAVE RESULTS"
        )

        result_file = save_results(
            transcript=aligned_segments,
            speaker_statistics=speaker_statistics,
            language=language,
            language_probability=language_probability,
            meeting_analysis=meeting_analysis
        )

        logger.info(
            "Results saved successfully: %s",
            result_file
        )

        # ----------------------------------------------------
        # FINAL RESULT
        # ----------------------------------------------------

        logger.info(
            "Meeting processing completed successfully."
        )

        logger.info(
            "================================================"
        )

        print(
            "\n========================================"
        )

        print(
            "PIPELINE COMPLETED SUCCESSFULLY"
        )

        print(
            "========================================"
        )

        print(
            f"Language: {language}"
        )

        print(
            f"Language probability: "
            f"{language_probability:.4f}"
        )

        print(
            f"Transcript segments: "
            f"{len(aligned_segments)}"
        )

        print(
            f"Result file: "
            f"{result_file}"
        )

        return {
            "language": language,
            "language_probability": language_probability,
            "transcript": aligned_segments,
            "speaker_statistics": speaker_statistics,
            "meeting_analysis": meeting_analysis,
            "result_file": str(result_file)
        }

    except Exception as error:

        # ----------------------------------------------------
        # ERROR LOGGING
        # ----------------------------------------------------

        logger.exception(
            "Meeting processing failed: %s",
            error
        )

        print(
            "\n========================================"
        )

        print(
            "PIPELINE FAILED"
        )

        print(
            "========================================"
        )

        print(
            f"Error: {error}"
        )

        raise


# ============================================================
# DIRECT EXECUTION
# ============================================================

if __name__ == "__main__":

    test_file = Path(
        "data/uploads/test_60sec.wav"
    )

    result = process_meeting(
        test_file
    )

    print(
        "\n=============================="
    )

    print(
        "CONFIDENCE SAMPLE"
    )

    print(
        "=============================="
    )

    for segment in result[
        "transcript"
    ][:5]:

        print(
            f"[{segment['start']:.2f}s - "
            f"{segment['end']:.2f}s] "
            f"{segment['speaker']} | "
            f"confidence/logprob: "
            f"{segment.get('confidence', 'N/A')} | "
            f"{segment['text']}"
        )