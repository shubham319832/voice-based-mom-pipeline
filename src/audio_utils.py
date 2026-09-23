import subprocess
from pathlib import Path


def convert_to_wav(input_file, output_file):
    """
    Convert audio/video into mono 16 kHz WAV using FFmpeg.
    """

    input_path = Path(input_file)
    output_path = Path(output_file)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    command = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_path),
        "-vn",
        "-ac",
        "1",
        "-ar",
        "16000",
        str(output_path)
    ]

    print("\n==============================")
    print("AUDIO PREPROCESSING")
    print("==============================")

    print("Input :", input_path)
    print("Output:", output_path)

    subprocess.run(command, check=True)

    print("\nAudio conversion completed successfully!")
    print("Saved to:", output_path)


if __name__ == "__main__":

    input_file = "data/uploads/test_meeting.mp4.mp4"
    output_file = "data/audio/meeting_audio.wav"

    convert_to_wav(
        input_file,
        output_file
    )