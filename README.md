# EduGenie — Google Gemini Powered Learning Assistant

A lightweight AI-powered educational assistant built with **FastAPI** and **Google Gemini**.
It offers five study features through a simple HTML/CSS interface.

| Feature | What it does |
|---|---|
| **Concept Explanation** | Breaks a topic down into beginner-friendly language |
| **Q&A** | Answers a general or academic question concisely |
| **Quiz Generation** | Produces 3 MCQs (4 options each) from a passage, as structured JSON |
| **Summarization** | Condenses a long passage into quick-revision notes |
| **Learning Path** | Builds a beginner→advanced plan with resources and step-by-step guidance |

## Project structure

```
EduGenie/
├── main.py                  # FastAPI app, REST endpoints, entry point
├── config.py                # Shared model client, API key, model settings
├── explanation_module.py    # Concept explanation logic
├── qna.py                   # Question answering
├── quiz_module.py           # Quiz generation
├── summary_module.py        # Summarization
├── learning_path.py         # Learning recommendations
├── templates/index.html     # HTML frontend (five per-feature forms)
├── static/style.css         # Styling (light + dark theme, responsive)
├── static/app.js            # Progressive enhancement: fetch() + Markdown + quiz reveal
├── requirements.txt         # Python dependencies
├── .env.example             # Template for your API key (copy to .env)
└── .env                     # Your key — NOT committed to git
```

## Setup

1. **Install Python 3.10+** and create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate          # Windows
   source venv/bin/activate       # macOS / Linux
   ```

2. **Install the dependencies** (run from inside `EduGenie`):
   ```bash
   cd EduGenie
   pip install -r requirements.txt
   ```

3. **Add your Gemini API key.** Get a free one at
   <https://aistudio.google.com/apikey>, then:
   ```bash
   copy .env.example .env         # Windows
   cp .env.example .env           # macOS / Linux
   ```
   and set `GEMINI_API_KEY=AQ.Ab8...` in `.env`.
   The key starts with `AQ.` or `AIza` — **not** `sk-` (that is an OpenAI key).

## Run

```bash
cd EduGenie
uvicorn main:app --reload
```
or simply `python main.py`. Then open <http://127.0.0.1:8000>.

> The app must be started from inside the `EduGenie` folder, because `main.py`
> loads `templates/`, `static/` and `.env` using relative paths.

## Using the web UI

The page shows **one form per feature**, stacked in this order: Ask a Question,
Get an Explanation, Summarize, Generate a Quiz, Build a Learning Path. Each form
has its own result panel, so answers never overwrite one another.

- With JavaScript enabled, `static/app.js` intercepts each form, calls the
  matching `/api/*` endpoint and renders the reply **in place** — no page reload.
  Model output is rendered as Markdown and is HTML-escaped first, so a reply can
  never inject markup into the page.
- With JavaScript disabled the forms fall back to a normal POST to `/process`,
  which re-renders the page with the result and the previous input restored.
- Useful extras: a dark-mode toggle (top-right, remembered in `localStorage`),
  a **Show correct answer** button per quiz question, and
  <kbd>Ctrl</kbd>/<kbd>Cmd</kbd> + <kbd>Enter</kbd> to submit from any input.

## REST API

| Method | Endpoint | Form field | Returns |
|---|---|---|---|
| GET | `/` | – | The frontend page |
| POST | `/process` | `task`, `user_input` | The frontend page with results |
| POST | `/api/explain` | `topic` | `{"result": "..."}` |
| POST | `/api/qa` | `question` | `{"result": "..."}` |
| POST | `/api/quiz` | `passage` | `{"quiz": [ ... ]}` |
| POST | `/api/summarize` | `passage` | `{"result": "..."}` |
| POST | `/api/learn` | `topic` | `{"result": "..."}` |

Interactive docs are available at <http://127.0.0.1:8000/docs>.

## Tests

```bash
cd EduGenie
python test_nojs_process.py
```

The suite stubs every model call, so it **uses no Gemini quota**. It boots the
real app on a free port and covers both paths: the no-JavaScript `/process`
form posts (result lands in the correct panel, input is restored, output is
HTML-escaped) and the `/api/*` endpoints `app.js` calls, plus a static check
that the template, `app.js` and `main.py` agree on task names and field names.

> Uses `urllib` rather than starlette's `TestClient` because the installed
> starlette (0.36.x) and httpx (0.28.x) versions are not compatible.

## Configuration

All of this lives in `.env` — no code changes needed:

| Variable | Default | Purpose |
|---|---|---|
| `GEMINI_API_KEY` | – | Required. Your Google AI Studio key |
| `GEMINI_MODEL` | `gemini-3.6-flash` | Gemini model to use |
| `LLM_PROVIDER` | `gemini` | `gemini` or `openai` |
| `OPENAI_API_KEY` | – | Only when `LLM_PROVIDER=openai` |
| `OPENAI_MODEL` | `gpt-4o-mini` | Only when `LLM_PROVIDER=openai` |
| `OPENAI_BASE_URL` | `https://api.openai.com/v1` | Any OpenAI-compatible gateway |

Transient Gemini capacity errors (`503` / `429`) are retried automatically up to
three times, then reported as a friendly message instead of a raw error.

## Notes

- `google-genai` is the current SDK; the retired `google-generativeai` is not used.
- The old `gemini-1.5-*` and `gemini-2.0-*` models have been shut down by Google.
- Never commit `.env` — it is already listed in `.gitignore`.