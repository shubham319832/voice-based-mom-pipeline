import json
from pathlib import Path


def save_results(
    transcript,
    speaker_statistics,
    language,
    language_probability,
    meeting_analysis
):
    """
    Save the complete meeting analysis as JSON.
    """

    output_directory = Path("data/results")

    output_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = (
        output_directory /
        "meeting_result.json"
    )

    result = {
        "language": language,
        "language_probability": round(
            language_probability,
            4
        ),
        "transcript": transcript,
        "speaker_statistics": speaker_statistics,
        "meeting_analysis": meeting_analysis
    }

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            result,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"\nResults saved successfully to: "
        f"{output_file}"
    )

    return output_file