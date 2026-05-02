# Textify - Backend

FastAPI Backend For Textify. Converts Between Images, Audio, PDFs, And Text Using Open-Source AI Models.

## How It Works

Send A File Or Text Payload Along With A Conversion Type, And The Server Routes It To The Appropriate Tool — Either A Local Model Or A Hugging Face Inference API Call — And Returns The Result As Text Or A Base64-Encoded Binary.

## Setup

1. Install Dependencies:

```bash
pip install -r requirements.txt
```

2. Create `.env` From The Example:

```bash
cp .env.example .env
```

3. Run The Server:

```bash
python -m uvicorn Main:App --reload --port 8000
```

Server Starts At `http://localhost:8000`.

## API

**`GET /`** — Health Check.

**`GET /conversions`** — List All Available Conversion Types With Metadata.

**`POST /convert`** — Perform A Conversion.

Request Body (`multipart/form-data`):

| Field             | Type   | Required | Description                              |
| ----------------- | ------ | -------- | ---------------------------------------- |
| `conversion_type` | String | Yes      | One Of The Supported Conversion IDs      |
| `file`            | File   | No       | Input File (Image, Audio, PDF, or Text)  |
| `text_input`      | String | No       | Input Text (For Text-Based Conversions)  |
| `options`         | String | No       | JSON String Of Additional Options        |

Response:

```json
{
  "type": "text",
  "content": "...",
  "filename": "output.txt",
  "mime_type": "text/plain"
}
```

For Binary Outputs (`type: "binary"`), `content` Is Base64-Encoded.

## Supported Conversions

| ID                   | Input  | Output      | Engine                              |
| -------------------- | ------ | ----------- | ----------------------------------- |
| `image_to_text`      | Image  | Text        | EasyOCR (Local)                     |
| `image_to_pdf`       | Image  | PDF         | EasyOCR + ReportLab (Local)         |
| `image_to_caption`   | Image  | Text        | BLIP (Local — `transformers`)       |
| `audio_to_text`      | Audio  | Text        | Whisper (HF Inference API)          |
| `pdf_to_text`        | PDF    | Text        | pypdf (Local)                       |
| `text_to_summary`    | Text   | Text        | BART (HF Inference API)             |
| `text_to_translation`| Text   | Text        | Helsinki-NLP (HF Inference API)     |
| `text_to_pdf`        | Text   | PDF         | ReportLab (Local)                   |
| `text_to_audio`      | Text   | Audio (WAV) | MMS-TTS (Local — `transformers`)    |

## Dependencies

| Package          | Version  |
| ---------------- | -------- |
| fastapi          | 0.115.12 |
| uvicorn          | 0.34.0   |
| python-multipart | 0.0.20   |
| python-dotenv    | 1.0.1    |
| requests         | 2.32.5   |
| easyocr          | 1.7.2    |
| numpy            | 2.4.2    |
| Pillow           | 12.2.0   |
| pypdf            | 6.7.5    |
| reportlab        | 4.5.0    |
| transformers     | 5.3.0    |
| scipy            | 1.17.1   |
| sentencepiece    | 0.2.1    |

## Models

| Model                                  | Task                | Source        |
| -------------------------------------- | ------------------- | ------------- |
| `openai/whisper-large-v3`              | Audio Transcription | HF Inference  |
| `Salesforce/blip-image-captioning-base`| Image Captioning    | Local         |
| `facebook/bart-large-cnn`              | Summarization       | HF Inference  |
| `Helsinki-NLP/opus-mt-en-{lang}`       | Translation         | HF Inference  |
| `facebook/mms-tts-eng`                 | Text To Speech      | Local         |

Local Models Are Downloaded On First Use And Cached By The `transformers` Library.

## Project Structure

```
backend/
├── Main.py                     — FastAPI App, CORS, Router Include
├── Routes.py                   — Route Handlers (HealthCheck, ListConversions, Convert)
├── Model.py                    — Conversions Registry And ConversionRouter Dispatcher
├── Tools/
│   ├── HFClient.py             — Hugging Face Inference API Client
│   ├── ImageToText.py          — Image OCR Using EasyOCR
│   ├── ImageToPDF.py           — Image To Searchable PDF
│   ├── ImageToCaption.py       — Image Captioning Using BLIP
│   ├── AudioToText.py          — Audio Transcription Using Whisper
│   ├── PDFToText.py            — PDF Text Extraction Using pypdf
│   ├── TextToSummary.py        — Text Summarization Using BART
│   ├── TextToTranslation.py    — Text Translation Using Helsinki-NLP
│   ├── TextToPDF.py            — Text To Formatted PDF
│   └── TextToAudio.py          — Text To Speech Using MMS-TTS
├── .env                        — Environment Config (Gitignored)
├── .env.example                — Environment Variable Reference
├── requirements.txt            — Dependencies
└── .gitignore
```