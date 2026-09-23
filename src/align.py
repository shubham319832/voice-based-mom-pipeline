def calculate_overlap(start1, end1, start2, end2):
    overlap_start = max(start1, start2)
    overlap_end = min(end1, end2)

    if overlap_start >= overlap_end:
        return 0.0

    return overlap_end - overlap_start


def assign_speaker(transcript_segment, speaker_segments):
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
    aligned_segments = []

    for transcript in transcript_segments:
        speaker = assign_speaker(
            transcript,
            speaker_segments
        )

        # Preserve all transcript information,
        # including confidence scores.
        aligned_segment = {
            "start": transcript["start"],
            "end": transcript["end"],
            "speaker": speaker,
            "text": transcript["text"]
        }

        if "confidence" in transcript:
            aligned_segment["confidence"] = transcript["confidence"]

        aligned_segments.append(aligned_segment)

    return aligned_segments


if __name__ == "__main__":

    transcript_segments = [
        {
            "start": 0.0,
            "end": 5.0,
            "text": "Hello everyone",
            "confidence": -0.15
        },
        {
            "start": 5.0,
            "end": 10.0,
            "text": "Today we will discuss AI",
            "confidence": -0.22
        }
    ]

    speaker_segments = [
        {
            "start": 0.0,
            "end": 6.0,
            "speaker": "SPEAKER_00"
        },
        {
            "start": 6.0,
            "end": 10.0,
            "speaker": "SPEAKER_01"
        }
    ]

    result = align_transcript(
        transcript_segments,
        speaker_segments
    )

    print("\n==============================")
    print("ALIGNMENT TEST")
    print("==============================")

    for segment in result:
        print(segment)