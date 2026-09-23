\# Voice-Based Minutes of Meeting (MoM) Pipeline



A local, AI-powered Voice-Based Minutes of Meeting pipeline that converts meeting audio/video into a structured transcript with speaker identification, timestamps, speaker statistics, and meeting analysis.



\## 1. Project Overview



This project processes recorded meetings and generates:



\- Speaker-wise transcript

\- Speaker identification

\- Start and end timestamps

\- Detected language and confidence

\- Speaker speaking duration

\- Speaker segment count

\- Speaker speaking percentage

\- Meeting summary

\- Key discussion points

\- Decisions

\- Action items

\- Structured JSON output



The pipeline is designed to support multilingual meeting recordings, including English, Hindi, and Odia, as required by the assignment.



The core voice-processing pipeline runs locally using open-source models and does not depend on paid external LLM APIs.



\---



\## 2. Architecture



```text

&#x20;                   Meeting Audio / Video

&#x20;                             |

&#x20;                             v

&#x20;                   FFmpeg Preprocessing

&#x20;                             |

&#x20;                             v

&#x20;                    16 kHz Mono WAV

&#x20;                             |

&#x20;                +------------+------------+

&#x20;                |                         |

&#x20;                v                         v

&#x20;         Whisper ASR              PyAnnote Diarization

&#x20;                |                         |

&#x20;                v                         v

&#x20;       Timestamped Transcript       Speaker Segments

&#x20;                |                         |

&#x20;                +------------+------------+

&#x20;                             |

&#x20;                             v

&#x20;                      Speaker Alignment

&#x20;                             |

&#x20;                             v

&#x20;                   Speaker Statistics

&#x20;                             |

&#x20;                             v

&#x20;                    Meeting Analysis

&#x20;                             |

&#x20;               +-------------+-------------+

&#x20;               |             |             |

&#x20;               v             v             v

&#x20;            Summary      Decisions    Action Items

&#x20;                             |

&#x20;                             v

&#x20;                      Structured JSON

&#x20;                             |

&#x20;                   +---------+---------+

&#x20;                   |                   |

&#x20;                   v                   v

&#x20;               Streamlit            FastAPI

&#x20;                  UI                  API


3. Technology Stack

Speech Recognition

Faster-Whisper

Whisper multilingual model

Model: small

CUDA GPU acceleration

Speaker Diarization

PyAnnote Audio

Model: pyannote/speaker-diarization-community-1

Audio Processing

FFmpeg

WAV

Mono audio

16 kHz sampling rate

Meeting Analysis

Python-based local rule-based analysis

Summary extraction

Discussion point extraction

Decision extraction

Action item extraction

User Interface

Streamlit

API

FastAPI

Uvicorn

Output

JSON

4\. Processing Pipeline

Step 1: Input



The application accepts:



MP4

WAV

MP3

M4A

WEBM

Step 2: Audio Preprocessing



FFmpeg converts the input into:



WAV format

Mono audio

16 kHz sampling rate

Step 3: Speech-to-Text



Faster-Whisper generates:



Transcript text

Start timestamp

End timestamp

Detected language

Language probability

Step 4: Speaker Diarization



PyAnnote identifies different speakers and generates anonymous labels such as:



SPEAKER\_00

SPEAKER\_01

SPEAKER\_02

Step 5: Speaker Alignment



Transcript segments are matched with speaker segments using temporal overlap.



Step 6: Speaker Statistics



The system calculates:



Speaking duration

Segment count

Speaking percentage

Step 7: Meeting Analysis



The local analysis module extracts:



Meeting summary

Key discussion points

Decisions

Action items

Step 8: Structured Output



The final result is stored as:



data/results/meeting\_result.json



The JSON contains:



Language information

Timestamped transcript

Speaker statistics

Meeting analysis

5\. Installation \& Setup

Prerequisites

Python 3.11

FFmpeg

NVIDIA GPU with CUDA support (recommended)

Hugging Face account for the PyAnnote diarization model

Create Virtual Environment

py -3.11 -m venv .venv



Activate the environment:



.\\.venv\\Scripts\\Activate.ps1

Install Dependencies

pip install -r requirements.txt

Hugging Face Authentication



The PyAnnote diarization model requires Hugging Face access.



Model:



pyannote/speaker-diarization-community-1



Before running the diarization pipeline:



Create or log in to a Hugging Face account.

Accept the model's usage conditions.

Create a Read access token.

Authenticate locally using the Hugging Face CLI.



Important: Never place the Hugging Face token directly in the source code or commit it to GitHub.



6\. Running the Streamlit Application



From the project root, run:



python -m streamlit run .\\src\\app.py



The application will open in the browser.



Upload a meeting recording and click:



Process Meeting



The application displays:



Detected language

Language confidence

Speaker statistics

Speaker-wise transcript

Meeting summary

Key discussion points

Decisions

Action items

JSON download

7\. Running the FastAPI Server



Start the API with:



python -m uvicorn src.api:app --reload



API address:



http://127.0.0.1:8000



Swagger API documentation:



http://127.0.0.1:8000/docs



Available endpoints:



GET  /

GET  /health

POST /process-meeting

8\. Output Structure



The generated result is saved as:



data/results/meeting\_result.json



Example:



{

&#x20;   "language": "en",

&#x20;   "language\_probability": 0.98,

&#x20;   "transcript": \[

&#x20;       {

&#x20;           "start": 25.73,

&#x20;           "end": 38.52,

&#x20;           "speaker": "SPEAKER\_00",

&#x20;           "text": "..."

&#x20;       }

&#x20;   ],

&#x20;   "speaker\_statistics": {

&#x20;       "SPEAKER\_00": {

&#x20;           "speaking\_duration\_seconds": 20.5,

&#x20;           "segment\_count": 2,

&#x20;           "speaking\_percentage": 80.0

&#x20;       }

&#x20;   },

&#x20;   "meeting\_analysis": {

&#x20;       "summary": "...",

&#x20;       "key\_discussion\_points": \[],

&#x20;       "decisions": \[],

&#x20;       "action\_items": \[]

&#x20;   }

}

9\. Multilingual Support



The project uses Whisper's multilingual speech recognition capabilities.



The pipeline is designed for:



English

Hindi

Odia

Multilingual and code-switched conversations



The detected language and language probability are included in the output.



Recognition quality may vary depending on:



Audio quality

Background noise

Speaker accent

Code-switching

Multiple speakers talking simultaneously

10\. Speaker Identification



The diarization system generates anonymous speaker labels such as:



SPEAKER\_00

SPEAKER\_01

SPEAKER\_02



These labels represent different speakers detected in the recording.



They do not represent the real-world names or identities of participants.



11\. Speaker Statistics



For each detected speaker, the system calculates:



Total speaking duration

Number of transcript segments

Percentage of total speaking time



Example:



{

&#x20;   "SPEAKER\_00": {

&#x20;       "speaking\_duration\_seconds": 35.2,

&#x20;       "segment\_count": 4,

&#x20;       "speaking\_percentage": 72.5

&#x20;   }

}

12\. Meeting Analysis



The current implementation uses local rule-based processing for meeting analysis.



It extracts:



Summary



A concise summary based on meaningful transcript content.



Key Discussion Points



Important transcript segments identified using meeting-related keywords.



Decisions



Statements indicating decisions or agreements.



Action Items



Statements indicating tasks, next steps, or responsibilities.



The current implementation does not require an external LLM API.



13\. Testing



The development pipeline was tested using a 60-second English meeting audio sample.

The following components were successfully tested:



Audio preprocessing

Whisper transcription

Language detection

PyAnnote speaker diarization

Speaker alignment

Speaker statistics

Meeting analysis

JSON generation

Streamlit interface

FastAPI health endpoint



The complete 60-second pipeline was successfully processed end-to-end.



14\. Limitations

Processing Time



Long meeting recordings require significant processing time because speech recognition and speaker diarization are performed locally.



Speaker Identification



The system generates anonymous speaker labels such as:



SPEAKER\_00



It does not identify the actual names of participants.



Meeting Analysis



The current summary, decision extraction, and action-item extraction use local rule-based processing.



Therefore, complex semantic reasoning may not always be captured accurately.



Overlapping Speech



Speaker alignment can become less accurate when multiple people speak simultaneously.



Multilingual Recognition



Whisper supports multilingual speech, but recognition accuracy depends on recording quality, language, accent, and background noise.



15\. Security and Privacy



The core voice pipeline does not require sending meeting recordings to external LLM APIs.



Meeting recordings and generated audio are excluded from Git using .gitignore.



Secrets such as Hugging Face tokens should never be committed to the repository.



16\. Future Improvements



Possible future enhancements include:



Improved overlap handling

Better language detection

Confidence scores

Timestamp visualization

Audio playback synchronized with transcript

PDF Minutes of Meeting export

DOCX Minutes of Meeting export

Batch processing

Background/async processing

Docker deployment

Automated tests

Improved semantic meeting summarization

Production logging and monitoring

17\. Project Structure

voice-mom-ai/

│

├── data/

│   ├── audio/

│   ├── results/

│   └── uploads/

│

├── src/

│   ├── align.py

│   ├── api.py

│   ├── app.py

│   ├── audio\_utils.py

│   ├── diarize.py

│   ├── meeting\_analysis.py

│   ├── meeting\_pipeline.py

│   ├── multilingual\_test.py

│   ├── pipeline.py

│   ├── save\_results.py

│   ├── stats.py

│   └── transcribe.py

│

├── .gitignore

├── requirements.txt

└── README.md

18\. Assignment Coverage



The project covers the core requirements of the Voice-Based Minutes of Meeting assignment:



Audio/video input

Audio preprocessing

Speech recognition

Speaker diarization

Speaker labels

Timestamped transcript

Speaker-wise transcript

Speaking statistics

Multilingual speech recognition capability (English, Hindi, and Odia through the Whisper multilingual model)Meeting summary

Discussion points

Decisions

Action items

Structured JSON output

Streamlit UI

FastAPI API

Local/open-source voice processing

