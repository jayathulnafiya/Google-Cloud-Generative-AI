# EduGenie document — corrections to match the code

**Purpose.** The project document describes three things the code does not do, references a model
that has been retired, and lists endpoint paths that differ from the implementation. This file gives
the **exact** original text and its replacement, in document order, so you can apply them in Word
with Find & Replace or by copy-pasting.

**Nothing here changes the code.** Every change makes the document describe what the code actually
does, so the report and the deliverable agree.

## Summary of changes

| # | Location in document | Problem | Fix |
|---|---|---|---|
| 1 | Project Description | Claims a local model ("local efficiency", "Mac M1") | Describe the single cloud Gemini client |
| 2 | Milestone 1, Activity 1.1 | Lists LaMini-Flan-T5-783M (local) — never used; and Gemini 1.5 Pro — retired | One model: `gemini-3.6-flash` |
| 3 | Folder Architecture | Missing `config.py` and `.env` | 11 entries instead of 9 |
| 4 | Milestone 2, item 1 (Explanation) | Says it uses LaMini-Flan-T5 | Say it uses Gemini |
| 5 | Milestone 2, item 2 (QnA) | "Gemini 1.5 Pro" | `gemini-3.6-flash` |
| 6 | Milestone 2, Activity 2.2 | `/qa`, `/explain`, `/quiz`, `/summarize`, `/learn/recommendations` | The real `/api/…` paths, plus `/` and `/process` |
| 7 | Exploring EduGenie, item 4 | "It corrects the answer if chosen wrong" — no such feature | Describe what the UI actually does |
| 8 | Milestone 4, Activity 4.1 | Missing `cd EduGenie` and dependency install | Add both steps |
| 9 | Pre-requisites | Never mentions `pip install -r requirements.txt` | Add a step 7 |
| 10 | Pre-requisites, Gemini API Key | Does not say where to store the key | Add `.env` location + key-format warning |

---

## 1. Project Description — line 11

**Original (delete):**

```
Built with FastAPI for the backend and a simple HTML+CSS frontend, EduGenie leverages lightweight and cloud-based AI models for local efficiency and cloud power. It works well on devices like the Mac M1, making it accessible to a broad range of learners and developers.
```

**Replacement (paste):**

```
Built with FastAPI for the backend and a simple HTML+CSS frontend, EduGenie leverages Google's cloud-based Gemini models through a single, lightweight API client. Because all inference happens in the cloud, the application ships no local model weights and requires no GPU, so it runs comfortably on ordinary laptops and accessible hardware, making EduGenie available to a broad range of learners and developers.
```

---

## 2. Milestone 1 — Activity 1.1: Select AI Models — lines 101–106

**Original (delete):**

```
* Gemini 1.5 Pro (via API):
Used for: Q&A, summarization, quiz generation, learning paths
Benefits: Advanced reasoning, structured outputs, and cloud inference
* LaMini-Flan-T5-783M (local):
Used for: Concept explanation
Benefits: Instruction-tuned, lightweight, CPU-compatible
```

**Replacement (paste):**

```
* Gemini (gemini-3.6-flash, via API):
Used for: Concept explanation, Q&A, summarization, quiz generation, and learning paths
Benefits: Advanced reasoning, reliable structured JSON output, a large context window, and cloud inference. All five features share one model and one API client, which keeps the codebase modular and easy to maintain.
```

> **Note:** Google has retired every `gemini-1.5-*` and `gemini-2.0-*` model, so `Gemini 1.5 Pro` can
> no longer be called. The code uses `gemini-3.6-flash` — a current, stable GA model, chosen in
> preference to the newest `gemini-3.8-flash` because the newest models frequently return
> `429 RESOURCE_EXHAUSTED` on free-tier API keys. The model name is read from the `GEMINI_MODEL`
> setting in `.env` (defaulting to `gemini-3.6-flash`), so it can be changed without editing any code.

---

## 3. Folder Architecture — lines 108–117

**Original (delete):**

```
EduGenie/
	   1. main.py                  # FastAPI app
	   2. explanation_module.py    # Concept explanation logic
	   3. qna.py                   # Question answering
	   4. quiz_module.py           # Quiz generation
	   5.  summary_module.py        # Summarization
	   6.  learning_path.py         # Learning recommendations
	   7.  templates/index.html     # HTML frontend
	   8.  static/style.css         # Styling
	   9.  requirements.txt         # Python dependencies
```

**Replacement (paste):**

```
EduGenie/
	   1.  main.py                  # FastAPI app and REST endpoints
	   2.  config.py                # Shared Gemini client, API key and model settings
	   3.  explanation_module.py    # Concept explanation logic
	   4.  qna.py                   # Question answering
	   5.  quiz_module.py           # Quiz generation
	   6.  summary_module.py        # Summarization
	   7.  learning_path.py         # Learning recommendations
	   8.  templates/index.html     # HTML frontend
	   9.  static/style.css         # Styling
	  10.  requirements.txt         # Python dependencies
	  11.  .env                    # GEMINI_API_KEY and GEMINI_MODEL (kept private)
```

> **Why:** `config.py` centralises the API key and the model name so the five feature modules no
> longer each hard-code them, and `.env` is the file that "securely stores" the API key mentioned in
> the pre-requisites.

---

## 4. Milestone 2 — Activity 2.1, item 1 (Explanation Module) — line 126

**Original (delete):**

```
EduGenie utilizes the LaMini-Flan-T5 model, a lightweight yet powerful generative AI, to deliver educational content in a simplified and highly readable manner. This model is specifically fine-tuned to provide concise, context-aware responses that break down complex topics into easily understandable language. By focusing on clarity and brevity, EduGenie ensures that learners with minimal background knowledge or technical experience can grasp essential concepts without feeling overwhelmed. This makes it particularly valuable for beginners, school students, or self-learners seeking straightforward explanations. The integration of LaMini-Flan-T5 empowers EduGenie to act as a reliable and accessible study companion for foundational learning across subjects.
```

**Replacement (paste):**

```
EduGenie utilizes Google's Gemini model to deliver educational content in a simplified and highly readable manner. The module builds a carefully engineered prompt that instructs the model to explain the requested concept in beginner-friendly, concise language, breaking complex topics down into a series of easily understandable points. By focusing on clarity and brevity, EduGenie ensures that learners with minimal background knowledge or technical experience can grasp essential concepts without feeling overwhelmed. This makes it particularly valuable for beginners, school students, or self-learners seeking straightforward explanations. The Gemini integration empowers EduGenie to act as a reliable and accessible study companion for foundational learning across subjects.
```

> **Why:** the module calls the Gemini API — the same shared client as the other four modules. No
> local model is loaded anywhere in the project.

---

## 5. Milestone 2 — Activity 2.1, item 2 (QnA Module) — line 131

Change **only the model name** in this paragraph:

| Find | Replace with |
|---|---|
| `EduGenie is powered by Gemini 1.5 Pro, enabling it to` | `EduGenie is powered by Google's Gemini model (gemini-3.6-flash), enabling it to` |

The rest of the paragraph stays exactly as written.

---

## 6. Milestone 2 — Activity 2.2: Backend API with FastAPI — lines 156–162

**Original (delete):**

```
   * Defined RESTful endpoints for each module:
   * /qa
   * /explain
   * /quiz
   * /summarize
   * /learn/recommendations
   * Connected each endpoint to a respective module logic
```

**Replacement (paste):**

```
   * Defined RESTful endpoints for each module:
   * POST /api/qa           # Question answering
   * POST /api/explain      # Concept explanation
   * POST /api/quiz         # Quiz generation (returns structured JSON)
   * POST /api/summarize    # Summarization
   * POST /api/learn        # Learning recommendations
   * GET  /                 # Serves the frontend (index.html)
   * POST /process          # Handles the HTML form and routes to the selected module
   * Connected each endpoint to a respective module logic
```

> **Two differences from the original text:** the module endpoints are namespaced under `/api`, and
> the learning-path endpoint is `/api/learn` (not `/learn/recommendations`). The last two entries are
> the routes the user actually interacts with through the browser.

---

## 7. Pre-requisites, item 4 (Google Gemini API Key) — line 63

**Original (delete):**

```
   3. Generate an API key and securely store it.
```

**Replacement (paste):**

```
   3. Generate an API key and securely store it in a .env file placed inside the EduGenie folder:
      GEMINI_API_KEY=your_key_here
   4. Note the key format: Gemini keys begin with AIza (Standard key) or AQ. (Auth key). A key
      beginning with sk- is an OpenAI key and will always be rejected by the Gemini API with
      "API key not valid". If the key is missing or invalid, EduGenie prints a clear warning at
      startup and shows the reason in the results panel instead of failing silently.
```

---

## 8. Pre-requisites — new item 7 (project dependencies) — insert after line 71

**Original (delete):**

```
6. Jinja2 (HTML Templating Engine)
* Official Documentation: Jinja2 Documentation
* Installation Steps:
   1. Install Jinja2 using pip: pip install jinja2
```

**Replacement (paste):**

```
6. Jinja2 (HTML Templating Engine)
* Official Documentation: Jinja2 Documentation
* Installation Steps:
   1. Install Jinja2 using pip: pip install jinja2
7. Project Dependencies (requirements.txt)
* Installation Steps:
   1. Open a terminal in the project folder and change into the application folder:
      cd EduGenie
   2. Install every pinned dependency in a single step:
      pip install -r requirements.txt
* This installs FastAPI, Uvicorn, Jinja2, python-multipart (required by FastAPI to parse HTML form
  submissions), python-dotenv (loads the .env file), pydantic, the Google Gen AI SDK used to call
  Gemini, and httpx (used by the optional OpenAI-compatible provider).
```

---

## 9. Milestone 4 — Activity 4.1: Run Locally — lines 188–189

**Original (delete):**

```
Run locally with uvicorn main:app --reload
Navigate to: http://127.0.0.1:8000
```

**Replacement (paste):**

```
Install the dependencies and start the server from inside the EduGenie folder:
    cd EduGenie
    pip install -r requirements.txt
    uvicorn main:app --reload      (or simply: python main.py)
Navigate to: http://127.0.0.1:8000
Note: the app must be launched from the EduGenie directory, because main.py loads the templates/ and
static/ folders and the .env file using relative paths. Running the command from the repository root
causes a "requirements.txt not found" error for the install step and a missing-templates error for
the server.
```

---

## 10. Exploring EduGenie, item 4 (Generating quizzes) — line 252

**Original (delete):**

```
It generates three questions with 4 options each. It corrects the answer if chosen wrong. 
```

**Replacement (paste):**

```
It generates three questions with 4 options each and displays the correct answer beneath each question for immediate self-checking, so learners can verify their understanding straight away.
```

> **Why:** the current interface renders the quiz as a read-only list — question, four options, and
> the correct answer. There are no option buttons, answer checking, or scoring in the frontend, so
> the words "corrects the answer if chosen wrong" overstate it. If you later add interactive quiz
> taking, this sentence can be restored.

---

## 11. Optional — running on an OpenAI-compatible endpoint (nothing to change for submission)

**This section requires no edit to the document.** The project ships with Gemini as the only active
provider, so every replacement above describes exactly what runs by default.

`config.py` also supports an OpenAI-compatible provider as a fallback — useful if the Gemini API is
unavailable, for example during a live demonstration. Turning it on needs **no code change**, only
these lines in `EduGenie\.env`:

```
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
OPENAI_BASE_URL=https://api.openai.com/v1
```

With `LLM_PROVIDER=openai`:

- the startup banner reads `EduGenie starting with OpenAI model: gpt-4o-mini`
- the required key variable becomes `OPENAI_API_KEY` (not `GEMINI_API_KEY`)
- all five features use the same prompts and behave identically
- `OPENAI_BASE_URL` can point at any OpenAI-compatible gateway

If you never set `LLM_PROVIDER`, none of this is active and the document stays exactly as written.
Only mention it in your report if you actually use it, since the pre-requisites and the model list
describe the Gemini path, which is the default.

---

## After applying the edits — quick self-check

Open the document and search for these strings; none should remain:

- `LaMini`  → should be 0 results (was 3 occurrences, spread over 2 lines)
- `Gemini 1.5`  → should be 0 results (was 2)
- `Mac M1`  → should be 0 results (was 1)
- `corrects the answer`  → should be 0 results (was 1)
- `/learn/recommendations`  → should be 0 results (was 1)

One more optional pass, if you want the document to be fully accurate:

- **Milestone 1, Activity 1.1** — the model-selection activity predates the decision to use one
  model. The replacement text in item 2 already handles this.
- **Challenges paragraph** (line 282) — it says "maintaining performance across devices" and
  "addressing data privacy concerns". Both are still fair, since the app runs entirely in the cloud.


