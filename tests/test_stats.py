from src.stats import calculate_speaker_statistics


def test_calculate_speaker_statistics():

    aligned_segments = [
        {
            "start": 0,
            "end": 10,
            "speaker": "SPEAKER_00",
            "text": "Hello"
        },
        {
            "start": 10,
            "end": 15,
            "speaker": "SPEAKER_01",
            "text": "Hi"
        },
        {
            "start": 15,
            "end": 20,
            "speaker": "SPEAKER_00",
            "text": "How are you?"
        }
    ]

    result = calculate_speaker_statistics(
        aligned_segments
    )

    assert "SPEAKER_00" in result
    assert "SPEAKER_01" in result

    assert result["SPEAKER_00"]["speaking_duration_seconds"] == 15

    assert result["SPEAKER_01"]["speaking_duration_seconds"] == 5

    assert result["SPEAKER_00"]["segment_count"] == 2

    assert result["SPEAKER_01"]["segment_count"] == 1

    assert result["SPEAKER_00"]["speaking_percentage"] == 75.0

    assert result["SPEAKER_01"]["speaking_percentage"] == 25.0


def test_empty_segments():

    result = calculate_speaker_statistics([])

    assert result == {}