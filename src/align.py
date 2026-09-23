def calculate_overlap(start1, end1, start2, end2):
    """
    Calculate how much two time intervals overlap.
    """
    overlap_start = max(start1, start2)
    overlap_end = min(end1, end2)

    if overlap_start >= overlap_end:
        return 0.0

    return overlap_end - overlap_start


def assign_speaker(transcript_segment, speaker_segments):
    """
    Assign the speaker whose diarization segment
    has the largest overlap with the transcript segment.
    """

    transcript_start = transcript_segment["start"]
    transcript_end = transcript_segment["end"]

    best_speaker = "UNKNOWN"
    best_overlap = 0.0

    for speaker_segment in speaker_segments:

        overlap = calculate_overlap(
            transcript_start,
            transcript_end,
            speaker_segment["start"],
            speaker_segment["end"]
        )

        if overlap > best_overlap:
            best_overlap = overlap
            best_speaker = speaker_segment["speaker"]

    return best_speaker


def align_transcript(transcript_segments, speaker_segments):
    """
    Combine transcript segments with speaker information.
    """

    aligned_segments = []

    for transcript in transcript_segments:

        speaker = assign_speaker(
            transcript,
            speaker_segments
        )

        aligned_segments.append({
            "start": transcript["start"],
            "end": transcript["end"],
            "speaker": speaker,
            "text": transcript["text"]
        })

    return aligned_segments


if __name__ == "__main__":

    # Small test to verify the alignment logic

    transcript_segments = [
        {
            "start": 10.0,
            "end": 15.0,
            "text": "Hello everyone."
        },
        {
            "start": 20.0,
            "end": 25.0,
            "text": "Today we will discuss AI."
        }
    ]

    speaker_segments = [
        {
            "start": 9.0,
            "end": 16.0,
            "speaker": "SPEAKER_00"
        },
        {
            "start": 19.0,
            "end": 26.0,
            "speaker": "SPEAKER_01"
        }
    ]

    result = align_transcript(
        transcript_segments,
        speaker_segments
    )

    print("\n===== ALIGNMENT TEST =====")

    for item in result:
        print(
            f"[{item['start']:.2f}s - {item['end']:.2f}s] "
            f"{item['speaker']}: "
            f"{item['text']}"
        )

    print("\n===== ALIGNMENT TEST COMPLETE =====")