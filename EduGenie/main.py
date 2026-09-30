from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import KEY_ENV_VAR, KEY_SETUP_URL, MODEL_IN_USE, PROVIDER_LABEL, get_api_key

# Fail loudly at startup instead of on the first user request.
if not get_api_key():
    print(
        f"WARNING: {KEY_ENV_VAR} is not set. Add it to EduGenie/.env "
        f"(create a key at {KEY_SETUP_URL}).",
        flush=True,
    )
else:
    print(f"EduGenie starting with {PROVIDER_LABEL} model: {MODEL_IN_USE}", flush=True)

from explanation_module import get_explanation
from qna import get_answer
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

app = FastAPI(title="EduGenie", description="Google Gemini Powered Learning Assistant")

# Mount Static and Templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})

@app.post("/process", response_class=HTMLResponse)
async def process_task(request: Request, task: str = Form(...), user_input: str = Form(...)):
    result = None
    quiz_data = None

    if task == "explain":
        result = get_explanation(user_input)
    elif task == "qa":
        result = get_answer(user_input)
    elif task == "quiz":
        quiz_data = generate_quiz(user_input)
    elif task == "summarize":
        result = summarize_text(user_input)
    elif task == "recommend":
        result = get_learning_recommendations(user_input)
    else:
        result = "Invalid task selected."

    return templates.TemplateResponse("index.html", {
        "request": request, 
        "result": result, 
        "quiz_data": quiz_data,
        "selected_task": task,
        "user_input": user_input
    })

# Explicit REST Endpoints as per Milestone 2
@app.post("/api/explain")
def api_explain(topic: str = Form(...)):
    return {"result": get_explanation(topic)}

@app.post("/api/qa")
def api_qa(question: str = Form(...)):
    return {"result": get_answer(question)}

@app.post("/api/quiz")
def api_quiz(passage: str = Form(...)):
    return {"quiz": generate_quiz(passage)}

@app.post("/api/summarize")
def api_summarize(passage: str = Form(...)):
    return {"result": summarize_text(passage)}

@app.post("/api/learn")
def api_learn(topic: str = Form(...)):
    return {"result": get_learning_recommendations(topic)}


if __name__ == "__main__":
    # Convenience: `python main.py` starts the same server as `uvicorn main:app`.
    # Run it from inside the EduGenie folder, because templates/, static/ and .env
    # are all resolved relative to the working directory.
    import uvicorn

    print("Starting EduGenie on http://127.0.0.1:8000  (press Ctrl+C to stop)", flush=True)
    uvicorn.run(app, host="127.0.0.1", port=8000)