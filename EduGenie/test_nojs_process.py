"""No-JavaScript acceptance test for the /process fallback.

Stubs every model call so no Gemini quota is used, serves the real app on a
free port via uvicorn, then POSTs each of the five forms the way a browser
without JS would and asserts the re-rendered page contains the answer inside
the correct panel.

Requests go through urllib rather than starlette's TestClient because the
installed starlette (0.36.x) and httpx (0.28.x) versions are incompatible.
"""
import json
import socket
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request

import uvicorn

import main

main.get_explanation = lambda t: f"EXPL::{t}"
main.get_answer = lambda q: f"ANS::{q}"
main.summarize_text = lambda t: f"SUM::{t}"
main.get_learning_recommendations = lambda t: f"REC::{t}"
main.generate_quiz = lambda t: [
    {"question": f"Q{i} about {t}?", "options": ["A", "B", "C", "D"], "answer": "B"}
    for i in (1, 2, 3)
]

def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


PORT = free_port()
server = uvicorn.Server(
    uvicorn.Config(main.app, host="127.0.0.1", port=PORT, log_level="error")
)
threading.Thread(target=server.run, daemon=True).start()

for _ in range(100):
    if server.started:
        break
    time.sleep(0.1)
else:
    sys.exit("server failed to start")

BASE = f"http://127.0.0.1:{PORT}"
checks, failures = 0, []


def check(label, cond):
    global checks
    checks += 1
    if not cond:
        failures.append(label)


def get(path):
    with urllib.request.urlopen(BASE + path, timeout=20) as r:
        return r.status, r.read().decode("utf-8")


def post_form(path, data):
    body = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(
        BASE + path, data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.status, r.read().decode("utf-8")


def panel(body, panel_id):
    """Extract a single output panel from the rendered HTML."""
    start = body.index(f'id="{panel_id}"')
    end = body.index("</section>", start)
    return body[start:end]


# --- GET / : every panel must start empty -----------------------------------
status, home = get("/")
check("GET / status 200", status == 200)
for pid in ("qaResult", "explanationResult", "summaryResult", "quizResult", "learnResult"):
    check(f"GET / {pid} empty", "markdown-output" not in panel(home, pid))
check("GET / no quiz items", 'class="quiz-item"' not in home)

# --- POST /process for each of the five tasks --------------------------------
cases = [
    ("qa", "Why is the sky blue?", "qaResult", "ANS::Why is the sky blue?"),
    ("explain", "Photosynthesis", "explanationResult", "EXPL::Photosynthesis"),
    ("summarize", "A long paragraph.", "summaryResult", "SUM::A long paragraph."),
    ("recommend", "SQL", "learnResult", "REC::SQL"),
]
for task, value, pid, expected in cases:
    status, body = post_form("/process", {"task": task, "user_input": value})
    check(f"{task} HTTP 200", status == 200)
    check(f"{task} result rendered in {pid}", expected in panel(body, pid))
    check(f"{task} input retained", f'value="{value}"' in body)
    # Result must appear in its own panel only, never in another one.
    others = [p for _, _, p, _ in cases if p != pid] + ["quizResult"]
    for other in others:
        check(f"{task} not leaked into {other}", expected not in panel(body, other))

# --- Quiz --------------------------------------------------------------------
status, body = post_form("/process", {"task": "quiz", "user_input": "Solar System"})
quiz_panel = panel(body, "quizResult")
check("quiz HTTP 200", status == 200)
check("quiz rendered 3 items", quiz_panel.count('class="quiz-item"') == 3)
check("quiz options rendered", quiz_panel.count("<li>") == 12)
check("quiz answer revealed", "Correct answer: B" in quiz_panel)
check("quiz question text", "Q1 about Solar System?" in quiz_panel)
check("quiz input retained", 'value="Solar System"' in body)
check("quiz has no JS-only button", "btn-reveal" not in quiz_panel)

# --- Escaping ----------------------------------------------------------------
main.get_answer = lambda q: "<script>alert(1)</script> & 'quotes'"
status, body = post_form("/process", {"task": "qa", "user_input": "xss"})
body = panel(body, "qaResult")
check("model HTML is escaped", "<script>" not in body and "&lt;script&gt;" in body)
check("ampersand escaped", "&amp;" in body)
main.get_answer = lambda q: f"ANS::{q}"

# --- Unknown task ------------------------------------------------------------
status, body = post_form("/process", {"task": "nope", "user_input": "x"})
check("unknown task HTTP 200", status == 200)
check("unknown task message", "Invalid task selected." in body)
check("unknown task not in a panel", "Invalid task selected." not in panel(body, "qaResult"))

# --- REST endpoints unchanged (what app.js calls) ---------------------------
def rest(path, field, value, key):
    status, body = post_form(path, {field: value})
    check(f"{path} HTTP 200", status == 200)
    return json.loads(body)[key]


check("api/qa", rest("/api/qa", "question", "q", "result") == "ANS::q")
check("api/explain", rest("/api/explain", "topic", "t", "result") == "EXPL::t")
check("api/summarize", rest("/api/summarize", "passage", "p", "result") == "SUM::p")
check("api/learn", rest("/api/learn", "topic", "t", "result") == "REC::t")
check("api/quiz", rest("/api/quiz", "passage", "p", "quiz")[0]["answer"] == "B")

# --- Validation --------------------------------------------------------------
try:
    post_form("/api/qa", {})
    check("missing field rejected", False)
except urllib.error.HTTPError as e:
    check("missing field -> 422", e.code == 422)

server.should_exit = True
print(f"{checks - len(failures)}/{checks} checks passed")
for f in failures:
    print("FAIL:", f)

# --- Static contract: template <-> app.js <-> main.py ----------------------
import re  # noqa: E402

tpl = open("templates/index.html", encoding="utf-8").read()
js = open("static/app.js", encoding="utf-8").read()
py = open("main.py", encoding="utf-8").read()

# Every form: hidden task value must match the one /process dispatches on.
tasks = set(re.findall(r'name="task" value="([^"]+)"', tpl))
dispatched = set(re.findall(r'task == "([^"]+)"', py))
static_checks, static_fail = 0, []


def scheck(label, cond):
    global static_checks
    static_checks += 1
    if not cond:
        static_fail.append(label)


scheck("template tasks == /process tasks", tasks == dispatched)

# Each data-api must exist as a route in main.py.
for api in re.findall(r'data-api="([^"]+)"', tpl):
    scheck(f"route {api} exists", f'"{api}"' in py)

# app.js must send the field name each endpoint declares.
endpoint_field = {
    "/api/qa": "question",
    "/api/explain": "topic",
    "/api/learn": "topic",
    "/api/summarize": "passage",
    "/api/quiz": "passage",
}
for api, field in endpoint_field.items():
    scheck(f"{api} expects {field}", re.search(rf'"{re.escape(api)}[^\n]*', py)
           and f'{field}: str = Form' in py.split(f'"{api}"')[1][:200])
    scheck(f"app.js maps {field}", f"{field}: value" in js)

# app.js and the template must agree on the quiz panel.
scheck("app.js renders quiz from data.quiz", 'data.quiz' in js)
scheck("quiz form data-key=quiz", 'data-key="quiz"' in tpl)
scheck("others use data-key=result", tpl.count('data-key="result"') == 4)

print(f"{static_checks - len(static_fail)}/{static_checks} static contract checks passed")
for f in static_fail:
    print("FAIL:", f)
sys.exit(1 if static_fail else 0)
