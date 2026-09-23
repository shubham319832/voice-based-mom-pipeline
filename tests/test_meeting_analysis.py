from src.meeting_analysis import analyze_meeting


def test_meeting_analysis():

    aligned_segments = [
        {
            "start": 0,
            "end": 5,
            "speaker": "SPEAKER_00",
            "text": "We discussed the project requirements."
        },
        {
            "start": 5,
            "end": 10,
            "speaker": "SPEAKER_01",
            "text": "We agreed to complete the project by Friday."
        },
        {
            "start": 10,
            "end": 15,
            "speaker": "SPEAKER_00",
            "text": "I will prepare the documentation."
        }
    ]

    result = analyze_meeting(
        aligned_segments
    )

    # Summary
    assert result["summary"] != ""

    # Key discussion points
    assert len(
        result["key_discussion_points"]
    ) > 0

    # Decision detection
    assert len(
        result["decisions"]
    ) > 0

    assert (
        "agreed"
        in result["decisions"][0]["text"].lower()
    )

    # Action item detection
    assert len(
        result["action_items"]
    ) > 0

    assert (
        "prepare"
        in result["action_items"][0]["text"].lower()
    )


def test_empty_meeting():

    result = analyze_meeting([])

    assert result["summary"] == ""

    assert result["key_discussion_points"] == []

    assert result["decisions"] == []

    assert result["action_items"] == []