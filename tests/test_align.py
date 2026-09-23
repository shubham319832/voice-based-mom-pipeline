from src.align import (
    calculate_overlap,
    assign_speaker,
    align_transcript
)


def test_calculate_overlap():
    result = calculate_overlap(
        0,
        10,
        5,
        15
    )

    assert result == 5


def test_calculate_overlap_no_overlap():
    result = calculate_overlap(
        0,
        5,
        10,
        15
    )

    assert result == 0.0


def test_assign_speaker():
    transcript_segment = {
        "start": 2,
        "end": 8,
        "text": "Hello"
    }

    speaker_segments = [
        {
            "start": 0,
            "end": 10,
            "speaker": "SPEAKER_00"
        },
        {
            "start": 10,
            "end": 20,
            "speaker": "SPEAKER_01"
        }
    ]

    result = assign_speaker(
        transcript_segment,
        speaker_segments
    )

    assert result == "SPEAKER_00"


def test_align_transcript_preserves_confidence():

    transcript_segments = [
        {
            "start": 0,
            "end": 5,
            "text": "Hello everyone",
            "confidence": -0.15
        }
    ]

    speaker_segments = [
        {
            "start": 0,
            "end": 5,
            "speaker": "SPEAKER_00"
        }
    ]

    result = align_transcript(
        transcript_segments,
        speaker_segments
    )

    assert len(result) == 1

    assert result[0]["speaker"] == "SPEAKER_00"

    assert result[0]["text"] == "Hello everyone"

    assert result[0]["confidence"] == -0.15