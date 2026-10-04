# عقد الفريق

## نوع الصوت المتفق عليه
np.ndarray أحادي (mono)، معدل 16000 Hz

## الدوال

### #1 معالجة صوتية
- load_audio(path) -> np.ndarray
- whisper_transcribe(audio) -> str

### #4 تحقق الهوية
- identity_score(audio) -> float (0.0 - 1.0)

### #5 كشف التزييف
- artifact_score(audio) -> float (0.0 - 1.0)
- detect_splice_points(audio) -> float (0.0 - 1.0)

### #4 + #5 (مشتركة)
analyze(identity_score, artifact_score, splice_score)
  -> { verdict: "موثّق" | "غير مؤكد" | "مزيّف", confidence: float }

## عقد API

### Request
POST /analyze
Content-Type: multipart/form-data
Body: file=<ملف صوتي>

### Response
{
  "transcript": "string",
  "identity_score": 0.85,
  "artifact_score": 0.10,
  "splice_score": 0.05,
  "verdict": "موثّق",
  "confidence": 0.88
}