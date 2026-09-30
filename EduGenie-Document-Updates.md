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

Items 9 and 10 patch single sentences. **Part 2 (items 13–15) supersedes both** with a full
rewrite of the Pre-requisites section, which additionally fixes two incorrect documentation
links and two items that have no installation steps at all. Apply Part 2 instead of 9 and 10.

| # | Location in document | Problem | Fix |
|---|---|---|---|
| 13 | Pre-requisites, item 1 (Python) | Cites *Google AI for Developers* and *Tom's Hardware* as Python documentation | Correct links (python.org, docs.python.org) + virtualenv step |
| 14 | Pre-requisites, items 2–6 | FastAPI and HTML/CSS have no installation steps; separate `pip install` per package cannot produce a working project | Consistent steps, each pointing at the single install command |
| 15 | Pre-requisites, new item 7 | Omits `python-multipart` and `python-dotenv` — without them the app cannot run | List all 8 pinned dependencies and what each one does |

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

## 12. Optional — running on an OpenAI-compatible endpoint (nothing to change for submission)

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

---

# PART 2 — Pre-requisites section (full rewrite)

The items above each correct a single sentence. The following three items replace the
**entire Pre-requisites block (document lines 39–71)** with a corrected version, because that
section contains wrong references, items with no installation steps, and omits two
dependencies the project genuinely needs.

> Apply items 7 and 8 (the single-sentence Pre-requisites fixes) **or** items 13–15 (the full
> Pre-requisites rewrite) — not both, since they cover the same document lines.

## Summary of Part 2

| Item | Document lines | What changes |
|---|---|---|
| 13 | 39–48 (item 1, Python) | Wrong documentation links: Google AI docs → python.org; Tom's Hardware → official guide |
| 14 | 51–71 (items 2–6) | Adds the missing installation steps for FastAPI, HTML/CSS and Gemini; corrects the Gemini key storage step |
| 15 | insert after 71 | New item 7: `requirements.txt` as the single install step, listing all 8 pinned dependencies |

---

## 13. Pre-requisites, item 1 (Python 3.10+) — document lines 39–48

**Original (delete):**

```
   1. Python 3.10+
* Official Documentation: Google AI for Developers
* Installation Guide: Tom's Hardware
* Popular Tutorial: Python Programming Tutorial - Full Course for Beginners
* Installation Steps:
1. Download the latest Python 3.10+ installer for your operating system from the official website.
2. Run the installer and ensure you check the box that says "Add Python to PATH".
3. Follow the installation prompts to complete the setup.
4. Verify the installation by opening a terminal or command prompt and typing python --version.
```

**Replacement (paste):**

```
1. Python 3.10+
* Official Documentation: https://docs.python.org/3/
* Official Download: https://www.python.org/downloads/
* Installation Guide: https://docs.python.org/3/using/windows.html
* Popular Tutorial: Python Programming Tutorial - Full Course for Beginners
* Installation Steps:
   1. Download the latest Python 3.10+ installer for your operating system from
      https://www.python.org/downloads/ and run it.
   2. On Windows, tick the box labelled "Add python.exe to PATH" before continuing.
      This is the option that allows python and pip to be run from any terminal.
   3. Follow the remaining installation prompts to complete the setup.
   4. Verify the installation by opening a terminal or command prompt and typing
      python --version. A version number of 3.10 or higher confirms a successful setup.
   5. Create an isolated virtual environment for the project so that its dependencies

---

## 14. Pre-requisites, items 2–6 (FastAPI, HTML & CSS, Gemini key, Uvicorn, Jinja2) — document lines 51–71

**Original (delete):**

```
2. FastAPI Framework – 
* Official Documentation: FastAPI
* User Guide: FastAPI
* Popular Tutorial: FastAPI Crash Course
3. HTML & CSS – Basic templating used in /templates and /static
4. Google Gemini API Key
* Official Documentation: Google AI for Developers
* Setup Guide: GeeksforGeeks
* Popular Tutorial: How to Use Google Gemini API Key
* Setup Steps:
   1. Visit the Google AI Studio and sign in with your Google account.
   2. Create a new project and enable the Gemini API.
   3. Generate an API key and securely store it.
5. Uvicorn (ASGI Server)
* Official Documentation: PyPI
* Installation Steps:
   1. Install Uvicorn using pip: pip install uvicorn
6. Jinja2 (HTML Templating Engine)
* Official Documentation: Jinja2 Documentation
* Installation Steps:
   1. Install Jinja2 using pip: pip install jinja2
```

**Replacement (paste):**

```
2. FastAPI Framework
* Official Documentation: https://fastapi.tiangolo.com/
* User Guide: https://fastapi.tiangolo.com/tutorial/
* Popular Tutorial: FastAPI Crash Course
* Role in EduGenie: provides the web server, the REST endpoints and the HTML page routing
* Installation Steps:
   1. Installed automatically with the other project dependencies, using the command in
      item 7 below:  pip install -r requirements.txt

3. HTML & CSS – Basic templating used in /templates and /static
* Official Documentation: https://developer.mozilla.org/en-US/docs/Web/HTML and
  https://developer.mozilla.org/en-US/docs/Web/CSS
* Role in EduGenie: the Jinja2 template templates/index.html renders the page, and
  static/style.css and static/app.js style it and give each feature its own form
* Installation Steps:
   1. No installation is required. HTML and CSS are plain text files that the browser
      renders, and both are already included in the project folder.

4. Google Gemini API Key
* Official Documentation: https://ai.google.dev/gemini-api/docs
* Key Management: https://aistudio.google.com/apikey
* Setup Steps:
   1. Visit the Google AI Studio at https://aistudio.google.com/apikey and sign in with
      your Google account.
   2. Click "Create API key", select or create a project, and confirm.
   3. Store the generated key in a file named .env placed inside the EduGenie folder:
        GEMINI_API_KEY=your_key_here
      The file is listed in .gitignore, so the key is never committed to version control.
      A ready-to-copy template is supplied as EduGenie/.env.example.
   4. Note the key format: Gemini keys begin with AIza (Standard key) or AQ. (Auth key).
      A key beginning with sk- is an OpenAI key and is always rejected by the Gemini API.

5. Uvicorn (ASGI Server)
* Official Documentation: https://www.uvicorn.org/
* PyPI: https://pypi.org/project/uvicorn/
* Installation Steps:
   1. Installed automatically with the other project dependencies, using the command in
      item 7 below:  pip install -r requirements.txt
   2. Start the application with:  uvicorn main:app --reload

---

## 15. Pre-requisites — new item 7 (installing the project) — insert after document line 71

This is the most important addition. The original Pre-requisites section never explains how to
install the project, and it omits two packages the application cannot run without.

**Original (delete):** nothing to delete — this item is inserted after item 6 (Jinja2).

**Replacement (paste):**

```
7. Project Dependencies (requirements.txt)
* Installation Steps:
   1. Open a terminal and change into the application folder, because requirements.txt is
      inside EduGenie and not in the project root:
        cd EduGenie
      Running this command from the parent folder produces
      "ERROR: Could not open requirements file: requirements.txt".
   2. Install every dependency in one step, from inside the EduGenie folder:
        pip install -r requirements.txt
   3. Start the application and open http://127.0.0.1:8000 in a browser:
        uvicorn main:app --reload
      Running "python main.py" from the same folder starts the same server.
* Packages installed:
   1. fastapi           - the web framework serving the page and the REST endpoints
   2. uvicorn           - the ASGI server that runs the application
   3. jinja2            - renders templates/index.html
   4. google-genai      - the Google Gen AI SDK used to call Gemini
   5. python-dotenv     - loads the API key from the .env file
   6. python-multipart  - required by FastAPI to read HTML form submissions. Without it
                          every "Get Answer", "Explain", "Summarize" and "Generate Quiz"
                          button fails with a server error.
   7. pydantic          - data validation used internally by FastAPI
   8. httpx             - HTTP client used by the optional OpenAI-compatible provider
```

> **Why:** the original list omits `python-multipart` and `python-dotenv` entirely, yet the
> application depends on both. `python-multipart` is the one that matters most: FastAPI raises a
> runtime error the moment a form field is read unless it is installed, so a reader who follows
> the original six items exactly would install the project and find that every button on the page
> fails. `python-dotenv` is equally required, since without it the API key in `.env` is never
> read and the application reports a missing key at startup. Both are therefore listed here
> rather than added to items 2–6, so the six technologies named in the document keep their
> original numbering.
>
> The `cd EduGenie` step is also stated explicitly, because `requirements.txt` sits inside the
> `EduGenie` folder rather than the project root. Installing from the parent folder fails with
> `Could not open requirements file`, which is the first error encountered when following the
> original document.
>
> The model name is not listed here because it is configuration, not a prerequisite. The
> application reads `GEMINI_MODEL` from `.env` and defaults to `gemini-3.6-flash`.

      Running python main.py from inside the EduGenie folder starts the same server.

6. Jinja2 (HTML Templating Engine)
* Official Documentation: https://jinja.palletsprojects.com/
* Installation Steps:
   1. Installed automatically with the other project dependencies, using the command in
      item 7 below:  pip install -r requirements.txt
```

> **Why:** item 3 (HTML & CSS) had no references and no installation steps at all, even though
> it is one of the six listed technologies. Items 2, 5 and 6 each install their package
> separately, which cannot produce a working project on its own — FastAPI additionally refuses
> to start without the form-parsing and template packages below, so installing it alone fails.
> The `pip install -r requirements.txt` command in item 7 is the real installation step for the
> whole project, and these entries now point to it instead of implying three separate installs.
> The Gemini key step is corrected to specify the `.env` file, because storing the key "securely"
> without saying where leaves the reader with no way to supply it, and a key placed in source
> code would be exposed publicly.

      do not affect the system Python:
         python -m venv venv
         venv\Scripts\activate          (Windows)
         source venv/bin/activate       (macOS / Linux)
      The prompt changes to (venv) when the environment is active.
```

> **Why:** the original credits *Google AI for Developers* as the official documentation for
> Python. That is Google's documentation, not Python's — the correct references are python.org
> and docs.python.org. Citing a third-party hardware site as the installation guide is also
> weaker than the official guidance, and the same document already uses official sources
> elsewhere, so the inconsistency stands out. Steps 5 and the PATH note are added because the
> project is developed inside a virtual environment, and a missing PATH entry is the single
> most common cause of `python` not being recognised in the terminal.
