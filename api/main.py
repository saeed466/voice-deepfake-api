from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import os
import traceback

app = FastAPI(title="Voice Deepfake Detector", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_FILE_SIZE = 25 * 1024 * 1024


def load_audio(path):
    return path

def whisper_transcribe(audio):
    return "نص تجريبي من Whisper"

def identity_score(audio):
    return 0.85

def artifact_score(audio):
    return 0.10

def detect_splice_points(audio):
    return 0.05


def analyze(id_s, art_s, spl_s):
    fake = max(art_s, spl_s)
    if fake >= 0.7 or id_s < 0.4:
        return {"verdict": "مزيّف", "confidence": round(fake, 2)}
    elif fake >= 0.4 or id_s < 0.7:
        return {"verdict": "غير مؤكد", "confidence": 0.5}
    else:
        return {"verdict": "موثّق", "confidence": round(id_s, 2)}


@app.get("/")
def root():
    return {"message": "Voice Deepfake Detector API", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyze")
async def analyze_endpoint(file: UploadFile = File(...)):
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(413, "حجم الملف يتجاوز 25MB")
    if len(contents) == 0:
        raise HTTPException(400, "الملف فارغ")

    suffix = os.path.splitext(file.filename or "audio.wav")[1] or ".wav"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(contents)
        tmp_path = tmp.name

    try:
        audio = load_audio(tmp_path)
        transcript = whisper_transcribe(audio)
        id_s = identity_score(audio)
        art_s = artifact_score(audio)
        spl_s = detect_splice_points(audio)
        result = analyze(id_s, art_s, spl_s)

        return {
            "transcript": transcript,
            "identity_score": round(id_s, 2),
            "artifact_score": round(art_s, 2),
            "splice_score": round(spl_s, 2),
            "verdict": result["verdict"],
            "confidence": result["confidence"],
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(500, f"خطأ: {str(e)}")
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)