from collections import defaultdict


def calculate_speaker_statistics(aligned_segments):
    """
    Calculate speaking statistics for each speaker.
    """

    speaker_duration = defaultdict(float)
    speaker_segment_count = defaultdict(int)

    for segment in aligned_segments:

        speaker = segment["speaker"]

        duration = segment["end"] - segment["start"]

        speaker_duration[speaker] += duration
        speaker_segment_count[speaker] += 1

    total_speaking_time = sum(
        speaker_duration.values()
    )

    statistics = {}

    for speaker in speaker_duration:

        duration = speaker_duration[speaker]

        if total_speaking_time > 0:
            percentage = (
                duration / total_speaking_time
            ) * 100
        else:
            percentage = 0

        statistics[speaker] = {
            "speaking_duration_seconds": round(
                duration, 2
            ),
            "segment_count": speaker_segment_count[speaker],
            "speaking_percentage": round(
                percentage, 2
            )
        }

    return statistics


if __name__ == "__main__":

    aligned_segments = [
        {
            "start": 0,
            "end": 10,
            "speaker": "SPEAKER_00",
            "text": "Hello everyone."
        },
        {
            "start": 10,
            "end": 20,
            "speaker": "SPEAKER_00",
            "text": "Today we will discuss AI."
        },
        {
            "start": 20,
            "end": 25,
            "speaker": "SPEAKER_01",
            "text": "Sounds good."
        }
    ]

    statistics = calculate_speaker_statistics(
        aligned_segments
    )

    print("\n===== SPEAKER STATISTICS =====")

    for speaker, stats in statistics.items():

        print(f"\n{speaker}")

        print(
            f"Speaking duration: "
            f"{stats['speaking_duration_seconds']} seconds"
        )

        print(
            f"Segments: "
            f"{stats['segment_count']}"
        )

        print(
            f"Speaking percentage: "
            f"{stats['speaking_percentage']}%"
        )

    print("\n===== STATISTICS TEST COMPLETE =====")