from pathlib import Path

from fastapi import FastAPI, File, UploadFile, HTTPException

from src.meeting_pipeline import process_meeting


app = FastAPI(
    title="Voice-Based Minutes of Meeting API",
    description="API for the Voice-Based Minutes of Meeting pipeline",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Voice-Based Minutes of Meeting API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/process-meeting")
async def process_meeting_api(
    file: UploadFile = File(...)
):

    allowed_extensions = {
        ".mp4",
        ".wav",
        ".mp3",
        ".m4a",
        ".webm"
    }

    file_extension = Path(
        file.filename
    ).suffix.lower()

    if file_extension not in allowed_extensions:

        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported file type. "
                "Use MP4, WAV, MP3, M4A, or WEBM."
            )
        )

    upload_directory = Path(
        "data/uploads"
    )

    upload_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    input_path = (
        upload_directory /
        file.filename
    )

    try:

        file_content = await file.read()

        with open(
            input_path,
            "wb"
        ) as output_file:

            output_file.write(
                file_content
            )

        result = process_meeting(
            input_file=input_path
        )

        return {
            "status": "success",
            "filename": file.filename,
            "result": result
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )