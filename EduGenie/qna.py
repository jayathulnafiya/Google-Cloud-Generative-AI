from config import generate_text

def get_answer(question: str) -> str:
    try:
        prompt = f"Answer the following educational question accurately and concisely: {question}"
        return generate_text(prompt)
    except Exception as e:
        return f"Error answering question: {str(e)}"