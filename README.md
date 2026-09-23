\# 🎙️ Voice-Based Minutes of Meeting Pipeline



An end-to-end Python-based Voice-to-Minutes-of-Meeting (MoM) pipeline that converts recorded meeting audio/video into a structured meeting record using local and open-source AI technologies.



The system performs speech transcription, speaker diarization, speaker-transcript alignment, speaker statistics, meeting analysis, and structured report generation.



It also provides a Streamlit web application, a FastAPI REST API, PDF export, automated tests, and centralized logging.



\---



\## 📌 Project Objective



The objective of this project is to build a voice-based Minutes of Meeting pipeline that analyzes recorded meetings and generates a structured output containing:



\- Speaker-wise transcript

\- Speaker identification using anonymous labels

\- Timestamped speech segments

\- Speaker speaking duration

\- Speaker participation statistics

\- Meeting summary

\- Key discussion points

\- Decisions

\- Action items

\- Detected language information



The pipeline is designed for multilingual meeting recordings and uses local/open-source models instead of paid external LLM APIs.



\---



\## 🏗️ System Architecture



```text

\&#x20;                   Meeting Audio / Video

\&#x20;                            │

\&#x20;                            ▼

\&#x20;                  ┌───────────────────┐

\&#x20;                  │  Audio / Video    │

\&#x20;                  │  Preprocessing    │

\&#x20;                  │     FFmpeg        │

\&#x20;                  └─────────┬─────────┘

\&#x20;                            │

\&#x20;                            ▼

\&#x20;                  ┌───────────────────┐

\&#x20;                  │  Speech-to-Text   │

\&#x20;                  │  Faster-Whisper   │

\&#x20;                  └─────────┬─────────┘

\&#x20;                            │

\&#x20;                            ▼

\&#x20;                  ┌───────────────────┐

\&#x20;                  │     Speaker       │

\&#x20;                  │    Diarization    │

\&#x20;                  │     pyannote      │

\&#x20;                  └─────────┬─────────┘

\&#x20;                            │

\&#x20;                            ▼

\&#x20;                  ┌───────────────────┐

\&#x20;                  │ Transcript +      │

\&#x20;                  │ Speaker Alignment │

\&#x20;                  └─────────┬─────────┘

\&#x20;                            │

\&#x20;                            ▼

\&#x20;                  ┌───────────────────┐

\&#x20;                  │ Speaker           │

\&#x20;                  │ Statistics        │

\&#x20;                  └─────────┬─────────┘

\&#x20;                            │

\&#x20;                            ▼

\&#x20;                  ┌───────────────────┐

\&#x20;                  │ Meeting Analysis  │

\&#x20;                  │                   │

\&#x20;                  │ Summary           │

\&#x20;                  │ Discussion Points │

\&#x20;                  │ Decisions         │

\&#x20;                  │ Action Items      │

\&#x20;                  └─────────┬─────────┘

\&#x20;                            │

\&#x20;                 ┌──────────┴──────────┐

\&#x20;                 │                     │

\&#x20;                 ▼                     ▼

\&#x20;         Structured JSON          PDF MoM Report

\&#x20;                 │

\&#x20;          ┌──────┴──────┐

\&#x20;          │             │

\&#x20;          ▼             ▼

\&#x20;      Streamlit      FastAPI

\&#x20;         UI             API

```



\---



\## 🧰 Technology Stack



| Component | Technology |

|---|---|

| Programming Language | Python 3.11 |

| Speech Recognition | Faster-Whisper |

| Speech Model | Whisper small |

| Speaker Diarization | pyannote.audio |

| Diarization Model | pyannote/speaker-diarization-community-1 |

| Audio Processing | FFmpeg |

| Web Interface | Streamlit |

| REST API | FastAPI |

| API Server | Uvicorn |

| Visualization | Plotly |

| PDF Generation | ReportLab |

| Testing | Pytest |

| Logging | Python logging |

| GPU Acceleration | NVIDIA CUDA |



\---



\## 🤖 AI Models



\### Speech Recognition



The project uses \*\*Faster-Whisper\*\* with the \*\*Whisper small\*\* multilingual model.



```text

faster-whisper

\&#x20;       │

\&#x20;       ▼

Whisper small

```



The transcription pipeline provides:



\- Transcribed text

\- Start timestamp

\- End timestamp

\- Detected language

\- Language probability

\- Average log probability for transcription segments



Whisper is a multilingual speech recognition model and supports multiple languages.



\#### Multilingual Support



The architecture supports multilingual meeting recordings, including:



\- English

\- Hindi

\- Odia



The Whisper multilingual model also supports language switching within a recording.



> \\\*\\\*Validation Note:\\\*\\\* The development sample used during testing was an English meeting recording. Hindi and Odia support is implemented through the multilingual Whisper model, but separate Hindi/Odia recordings were not independently benchmarked during development.



\### 👥 Speaker Diarization



Speaker diarization is implemented using:



```text

pyannote/speaker-diarization-community-1

```



The system detects different speakers and assigns anonymous speaker labels such as:



```text

SPEAKER\\\_00

SPEAKER\\\_01

SPEAKER\\\_02

```



These labels represent consistent speaker identities within a recording. They do \*\*not\*\* identify the actual names of meeting participants.



\*\*Example:\*\*



```text

\\\[25.73s - 38.52s] SPEAKER\\\_00

\\\[34.41s - 34.56s] SPEAKER\\\_01

\\\[38.86s - 49.02s] SPEAKER\\\_00

```



The diarization component also demonstrated overlapping speaker activity during testing.



\### 🔗 Transcript and Speaker Alignment



After transcription and speaker diarization, the pipeline aligns every transcription segment with the speaker having the greatest temporal overlap.



```json

{

\&#x20;   "start": 13.2,

\&#x20;   "end": 17.88,

\&#x20;   "speaker": "SPEAKER\\\_00",

\&#x20;   "text": "So we are going to learn what is AI and what is ML.",

\&#x20;   "confidence": -0.3071

}

```



```text

Whisper Transcript

\&#x20;       +

Speaker Diarization

\&#x20;       ↓

Speaker-Attributed Transcript

```



The transcription log probability is also preserved through alignment.



\---



\## 📊 Speaker Statistics



The system calculates speaker-level participation statistics.



For each speaker, the pipeline calculates:



\- Speaking duration

\- Number of transcript segments

\- Speaking percentage



\*\*Example:\*\*



```json

{

\&#x20;   "SPEAKER\\\_00": {

\&#x20;       "speaking\\\_duration\\\_seconds": 45.2,

\&#x20;       "segment\\\_count": 8,

\&#x20;       "speaking\\\_percentage": 72.4

\&#x20;   }

}

```



This provides a quantitative view of participant involvement in the meeting.



\---



\## 📈 Speaker Timeline



The Streamlit application provides a visual speaker activity timeline using Plotly.



The timeline displays:



\- Speaker

\- Start time

\- End time

\- Segment duration



This helps visualize when different participants were speaking throughout the meeting.



\---



\## 📋 Meeting Analysis



The project performs local meeting analysis without relying on external LLM APIs. The analysis contains four sections:



\### 1. Meeting Summary



A concise summary generated from the available transcript.



\### 2. Key Discussion Points



The system identifies transcript segments containing relevant meeting/discussion keywords, e.g. topics related to projects, requirements, issues, training, deadlines, planning, AI/ML, and general discussions.



\### 3. Decisions



The system identifies explicit decision statements such as:



\- "We agreed to..."

\- "We decided..."

\- "The decision is..."

\- "Approved..."

\- "Confirmed..."



\### 4. Action Items



The system identifies action-oriented statements such as:



\- "We need to..."

\- "I will..."

\- "We will..."

\- "Should..."

\- "Must..."

\- "Next step..."

\- "Action item..."



> This analysis is intentionally implemented using \\\*\\\*local, deterministic/rule-based processing\\\*\\\* rather than an external generative LLM.



\---



\## 📄 PDF Export



The project includes PDF report generation using \*\*ReportLab\*\*.



The generated PDF contains:



\- Meeting language

\- Language probability

\- Number of speakers

\- Number of transcript segments

\- Speaker statistics

\- Meeting summary

\- Key discussion points

\- Decisions

\- Action items

\- Full speaker-wise transcript

\- Timestamps

\- Transcription log probability



Generated file:



```text

data/results/meeting\\\_mom.pdf

```



\---



\## ⚡ Quick Start



```powershell

git clone https://github.com/shubham319832/voice-based-mom-pipeline.git

cd voice-based-mom-pipeline

py -3.11 -m venv .venv

.\\\\.venv\\\\Scripts\\\\Activate.ps1

pip install -r requirements.txt

streamlit run src/app.py

```



Streamlit will display a local URL similar to:



```text

http://localhost:8501

```



Open this URL in your browser.



\---



\## ⚙️ Installation



\### 1. Clone the repository



```powershell

git clone https://github.com/shubham319832/voice-based-mom-pipeline.git

cd voice-based-mom-pipeline

```



\### 2. Create a virtual environment



Python 3.11 is recommended.



```powershell

py -3.11 -m venv .venv

```



\### 3. Activate the virtual environment



Windows PowerShell:



```powershell

.\\\\.venv\\\\Scripts\\\\Activate.ps1

```



\### 4. Install dependencies



```powershell

pip install -r requirements.txt

```



\---



\## 🚀 How to Use



The application can be used through the Streamlit interface, the FastAPI REST API, or directly through the Python pipeline.



\### Option 1 — Streamlit Web Application



The easiest way to use and demonstrate the project.



\*\*Step 1 — Start Streamlit\*\*



```powershell

streamlit run src/app.py

```



\*\*Step 2 — Open the application\*\*



```text

http://localhost:8501

```



\*\*Step 3 — Upload a meeting recording\*\*



Click \*\*Upload Meeting Audio / Video\*\*. Supported formats:



\- MP4

\- WAV

\- MP3

\- M4A

\- WEBM



\*\*Step 4 — Process the meeting\*\*



Click \*\*🚀 Process Meeting\*\*. The pipeline automatically runs:



```text

Upload

\&#x20;  ↓

Audio Preprocessing

\&#x20;  ↓

Speech Transcription

\&#x20;  ↓

Speaker Diarization

\&#x20;  ↓

Speaker Alignment

\&#x20;  ↓

Speaker Statistics

\&#x20;  ↓

Meeting Analysis

\&#x20;  ↓

Structured Results

```



\*\*Step 5 — Review the results\*\*



The application displays:



\- Detected language

\- Language probability

\- Speaker statistics

\- Speaker timeline

\- Speaker-wise transcript

\- Timestamp information

\- Transcription log probability

\- Meeting summary

\- Key discussion points

\- Decisions

\- Action items



\*\*Step 6 — Download the result\*\*



The Streamlit application provides a button to download `meeting\\\_result.json`.



\### Option 2 — FastAPI



The project also provides a REST API for programmatic integration.



\*\*Step 1 — Start the API\*\*



```powershell

uvicorn src.api:app --reload

```



\*\*Step 2 — Open Swagger UI\*\*



```text

http://127.0.0.1:8000/docs

```



\*\*Step 3 — Check API health\*\*



```text

GET /health

```



Expected response:



```json

{

\&#x20;   "status": "healthy"

}

```



\*\*Step 4 — Process a meeting\*\*



```text

POST /process-meeting

```



Upload an audio/video file using the Swagger interface. The endpoint accepts the uploaded meeting file and returns the structured meeting-processing result as JSON.



\### Option 3 — Run the Pipeline Directly



The core pipeline can also be executed directly from the terminal.



```powershell

python .\\\\src\\\\meeting\\\_pipeline.py

```



The pipeline performs:



```text

Input Validation

\&#x20;      ↓

Audio Conversion

\&#x20;      ↓

Whisper Transcription

\&#x20;      ↓

Speaker Diarization

\&#x20;      ↓

Speaker/Transcript Alignment

\&#x20;      ↓

Speaker Statistics

\&#x20;      ↓

Meeting Analysis

\&#x20;      ↓

JSON Result

```



The structured result is saved to:



```text

data/results/meeting\\\_result.json

```



\---



\## 📄 Generate the PDF Report



After a meeting result has been generated, run:



```powershell

python .\\\\src\\\\pdf\\\_export.py

```



The PDF report will be generated at:



```text

data/results/meeting\\\_mom.pdf

```



\---



\## 🧪 Automated Testing



The project uses \*\*Pytest\*\*.



\*\*Current test suite:\*\* 8 tests, 8 passed.



Tests cover:



\- \*\*Alignment\*\* — overlap calculation, no-overlap calculation, speaker assignment, confidence preservation

\- \*\*Meeting Analysis\*\* — summary/decision/action-item extraction, empty meeting handling

\- \*\*Statistics\*\* — speaker statistics, empty segment handling



Run:



```powershell

python -m pytest .\\\\tests -v

```



Expected result:



```text

8 passed

```



\---



\## 📝 Logging and Error Handling



The project includes centralized logging using Python's built-in `logging` module.



Log file:



```text

data/logs/pipeline.log

```



The pipeline logs important processing stages including:



\- Pipeline start

\- Audio preprocessing

\- Whisper model loading

\- Transcription

\- Diarization

\- Alignment

\- Speaker statistics

\- Meeting analysis

\- Result saving

\- Pipeline completion

\- Exceptions and tracebacks



Example:



```text

2026-09-23 14:44:48 | INFO | voice\\\_mom\\\_pipeline |

Voice-Based Minutes of Meeting logging system started.

```



\---



\## 📦 Output Structure



The primary JSON result is saved as:



```text

data/results/meeting\\\_result.json

```



The structure is:



```json

{

\&#x20;   "language": "en",

\&#x20;   "language\\\_probability": 0.9004,

\&#x20;   "transcript": \\\[],

\&#x20;   "speaker\\\_statistics": {},

\&#x20;   "meeting\\\_analysis": {

\&#x20;       "summary": "",

\&#x20;       "key\\\_discussion\\\_points": \\\[],

\&#x20;       "decisions": \\\[],

\&#x20;       "action\\\_items": \\\[]

\&#x20;   }

}

```



\### 📝 Sample Transcript Structure



```json

{

\&#x20;   "start": 0.0,

\&#x20;   "end": 13.2,

\&#x20;   "speaker": "SPEAKER\\\_00",

\&#x20;   "text": "Hello everyone, so today we are going to start with AI and ML.",

\&#x20;   "confidence": -0.3071

}

```



> \\\*\\\*Note:\\\*\\\* The `confidence` field represents Whisper's average log probability for the segment. It is \\\*\\\*not\\\*\\\* a percentage — e.g. `confidence = -0.3071` should be read as a log-probability value, not `30.71%`.



\---



\## 🔒 External LLM/API Policy



The core voice pipeline does \*\*not\*\* depend on paid external LLM APIs.



The implementation does not require:



\- OpenAI API

\- Gemini API

\- Claude API

\- Groq API

\- Other paid external LLM APIs



Speech recognition, speaker diarization, transcription, and meeting analysis are performed locally using open-source models/libraries and deterministic processing.



This follows the assignment requirement that the core voice pipeline must not depend on paid/external LLM APIs or API keys.



\---



\## 🖥️ Hardware and Environment



The development environment used:



\- \*\*Operating System:\*\* Windows

\- \*\*Python:\*\* 3.11.9

\- \*\*GPU:\*\* NVIDIA GeForce RTX 3050 Laptop GPU

\- \*\*VRAM:\*\* 4 GB

\- \*\*CUDA:\*\* 12.6

\- \*\*PyTorch:\*\* 2.14.0+cu126



The project uses GPU acceleration for the Whisper transcription workload.



For Windows environments, CUDA-related DLL directories may need to be made available to the Python process. The current implementation explicitly adds the required NVIDIA CUDA DLL directories when available.



\---



\## 🔐 Hugging Face Authentication



The pyannote diarization model requires access through Hugging Face.



Before running diarization:



1\. Create a Hugging Face account.

2\. Accept the model's usage conditions.

3\. Create a Hugging Face access token.

4\. Authenticate locally.



Example:



```powershell

hf auth login

```



> ⚠️ Do not commit access tokens or other secrets to GitHub.



\---



\## 📁 Project Structure



```text

voice-based-mom-pipeline/

│

├── data/

│   ├── audio/

│   ├── logs/

│   ├── results/

│   └── uploads/

│

├── models/

│

├── src/

│   ├── align.py

│   ├── api.py

│   ├── app.py

│   ├── audio\\\_utils.py

│   ├── diarize.py

│   ├── logger.py

│   ├── meeting\\\_analysis.py

│   ├── meeting\\\_pipeline.py

│   ├── multilingual\\\_test.py

│   ├── pdf\\\_export.py

│   ├── save\\\_results.py

│   └── stats.py

│

├── tests/

│   ├── test\\\_align.py

│   ├── test\\\_meeting\\\_analysis.py

│   └── test\\\_stats.py

│

├── .gitignore

├── README.md

└── requirements.txt

```



\---



\## 📋 Assignment Requirements Coverage



\### Core Requirements



\- \[x] Audio/video input

\- \[x] Audio preprocessing

\- \[x] Speech-to-text transcription

\- \[x] Speaker diarization

\- \[x] Speaker labels

\- \[x] Timestamped transcript

\- \[x] Speaker/transcript alignment

\- \[x] Speaker speaking duration

\- \[x] Speaker segment count

\- \[x] Speaker speaking percentage

\- \[x] Structured transcript

\- \[x] Meeting summary

\- \[x] Key discussion points

\- \[x] Decisions

\- \[x] Action items

\- \[x] Language information

\- \[x] Streamlit interface

\- \[x] FastAPI interface

\- \[x] Error handling

\- \[x] Automated tests



\### Bonus Features



\- \[x] Speaker overlap support through diarization

\- \[x] Language detection through Whisper

\- \[x] Transcription log probability

\- \[x] Speaker timeline visualization

\- \[x] PDF report generation

\- \[x] Automated tests

\- \[x] Pipeline logging

\- \[x] Error/exception logging



\---



\## 🧪 Development Validation



| Component | Result |

|---|---|

| Python environment | ✅ |

| NVIDIA GPU detection | ✅ |

| CUDA availability | ✅ |

| Faster-Whisper transcription | ✅ |

| Speaker diarization | ✅ |

| Speaker overlap detection | ✅ |

| Transcript alignment | ✅ |

| Speaker statistics | ✅ |

| Meeting analysis | ✅ |

| Confidence/log probability | ✅ |

| Streamlit pipeline | ✅ |

| FastAPI startup | ✅ |

| FastAPI health endpoint | ✅ |

| PDF generation | ✅ |

| Automated tests | ✅ 8/8 |

| Logging | ✅ |



\---



\## ⚠️ Current Limitations



\### 1. Speaker Identity



The system identifies speakers using anonymous labels (`SPEAKER\\\_00`, `SPEAKER\\\_01`, ...). It does not identify the actual names of participants.



\### 2. Multilingual Validation



The architecture supports multilingual Whisper transcription, including English, Hindi, and Odia. However, the available development sample was validated using English speech only — separate Hindi/Odia recordings were not independently benchmarked.



\### 3. Full Long-Meeting Validation



A 12-minute meeting recording was used during development, and audio preprocessing successfully converted it. A shorter 60-second development sample was used for repeated end-to-end testing because speaker diarization was computationally expensive on the available laptop GPU.



\### 4. Rule-Based Meeting Analysis



Summary, discussion-point, decision, and action-item extraction currently use deterministic/rule-based processing rather than an external generative LLM. This keeps the implementation compliant with the assignment's external-LLM restriction, but the generated meeting summary may be less semantically sophisticated than an LLM-generated summary.



\### 5. Speaker Overlap



The diarization system can detect overlapping speaker activity, but overlapping speech can make transcript-to-speaker alignment more challenging, since a transcript segment may contain speech from multiple speakers.



\---



\## 🚀 Future Improvements



\- Better semantic meeting summarization using a compliant local LLM

\- Improved Hindi/Odia validation and benchmarking

\- More robust action-item extraction

\- Improved decision extraction

\- Automatic language-switching detection

\- Speaker name mapping

\- Audio playback synchronized with transcript timestamps

\- DOCX export

\- Batch meeting processing

\- Asynchronous job processing

\- Docker deployment

\- Production monitoring

\- More extensive integration/API tests

\- Improved overlap-aware transcript attribution



\---



\## 🔒 Security and Privacy



The core processing is designed to run locally. Meeting recordings may contain sensitive information, so:



\- Do not commit meeting recordings to GitHub.

\- Do not commit API tokens or Hugging Face tokens.

\- Keep `.env` and credential files out of source control.

\- Review generated meeting reports before sharing them.



The repository `.gitignore` excludes uploaded meeting files, generated audio, generated results, logs, and environment files.



\---



\## 📌 Important Notes



\- \*\*Anonymous speaker labels:\*\* `SPEAKER\\\_00`, `SPEAKER\\\_01`, etc. are diarization outputs and should not be interpreted as verified participant identities.

\- \*\*Transcription confidence:\*\* Whisper's average log probability should not be treated as a percentage-based confidence score.

\- \*\*Human review:\*\* Generated summaries, decisions, and action items should be reviewed by a human before being treated as an official meeting record.



\---



GitHub: \[https://github.com/shubham319832/voice-based-mom-pipeline](https://github.com/shubham319832/voice-based-mom-pipeline)

