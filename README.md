# Ollama Text Summarizer (FastAPI + Gradio + Ollama)

Turn long text into crisp bullet-point summaries using a modern, local-first stack:

- FastAPI (async) backend wrapping Ollama
- Gradio UI for quick, friendly usage
- Pluggable local models via Ollama (use any model you've pulled locally)

---

## 🔥 Features
- **Local-first**: Runs against your local Ollama instance
- **Async + Typed API**: Pydantic request/response models, robust error handling
- **Gradio UI**: Slider to choose bullet count, clean UX
- **Config via env**: `OLLAMA_URL`, `MODEL_NAME`, `HTTP_TIMEOUT`
- **CORS + Health**: Ready for browser clients and basic monitoring

---

## 🧩 Architecture
- `app.py` — FastAPI service exposing `POST /summarize/`
- `text_summarizer.py` — Gradio UI that calls Ollama directly
- `requirements.txt` — Pinned dependencies

You can use either the API programmatically or the Gradio app interactively.

---

## ⚙️ Requirements
- Python 3.10+
- [Ollama](https://ollama.com/) installed and running locally
- At least one Ollama model pulled locally (e.g., `llama3:latest`, `qwen2:7b`, `phi3:mini`)

Install Python deps:
```bash
pip install -r requirements.txt
```

Pull a model once (examples):
```bash
# pick any model you prefer
ollama pull llama3:latest
# or
ollama pull qwen2:7b
# or
ollama pull phi3:mini
```

---

## 🚀 Run the FastAPI service
Start the API:
```bash
uvicorn app:app --reload
```

Health check:
```bash
curl http://127.0.0.1:8000/health
```

Summarize text:
```bash
curl -X POST http://127.0.0.1:8000/summarize/ \
  -H "Content-Type: application/json" \
  -d '{
        "text": "Artificial Intelligence is transforming...",
        "bullets": 3
      }'
```

Example JSON response:
```json
{
  "summary": "- Bullet 1...\n- Bullet 2...\n- Bullet 3..."
}
```

---

## 🖥️ Run the Gradio app
Launch the UI:
```bash
python text_summarizer.py
```
This starts a local web UI. Paste your text, choose bullet count, and click "Summarize".

---

## 🔧 Configuration (Environment Variables)
- `OLLAMA_URL` (default: `http://localhost:11434/api/generate`)
- `MODEL_NAME` (set to your local model tag, e.g., `llama3:latest`, `qwen2:7b`, `phi3:mini`)
- `HTTP_TIMEOUT` (default: `60`)

Examples:
```bash
export OLLAMA_URL=http://localhost:11434/api/generate
export MODEL_NAME=llama3:latest
export HTTP_TIMEOUT=90
```

---

## 📡 API Details
- `POST /summarize/` — Generate a bullet-point summary
  - Request body (JSON):
    ```json
    {
      "text": "string",
      "bullets": 3
    }
    ```
  - Response body (JSON):
    ```json
    {
      "summary": "string"
    }
    ```
- `GET /health` — Health check
- `GET /` — Service metadata

---

## 🛡️ Notes & Tips
- If you run this behind a reverse proxy, lock down CORS in `app.py` to specific origins.
- For production, consider request limits, auth, and observability.
- Gradio is great for demos; the FastAPI service is ideal for programmatic/automation.

---

## 🗺️ Roadmap
- Model selector in UI (switch between local models)
- Streaming responses
- Dockerfile + CI
- Basic tests for API contract

---

## 📜 License
MIT (or your preferred license)
