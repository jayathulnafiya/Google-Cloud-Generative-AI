from config import generate_text
import json
import re

def clean_json_block(text: str) -> str:
    # Cleans Markdown code blocks if present
    text = re.sub(r'^```json\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'^```\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s*```$', '', text)
    return text.strip()

def generate_quiz(passage: str):
    raw_text = ""
    try:
        prompt = (
            f"Based on the following passage, generate exactly 3 multiple-choice questions (MCQs). "
            f"Each question must contain four options and a correct answer. "
            f"Output strictly in JSON format as a list of objects with keys: 'question', 'options' (list of 4 strings), and 'correct_answer'.\n\n"
            f"Passage: {passage}"
        )
        raw_text = generate_text(prompt)
        quiz_data = json.loads(clean_json_block(raw_text))
        return quiz_data
    except Exception as e:
        return {"error": f"Failed to generate quiz: {str(e)}", "raw": raw_text}