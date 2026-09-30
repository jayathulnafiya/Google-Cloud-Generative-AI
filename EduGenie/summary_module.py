from config import generate_text

def summarize_text(passage: str) -> str:
    try:
        prompt = f"Summarize the following educational passage into a concise version suitable for quick revision, retaining core info:\n\n{passage}"
        return generate_text(prompt)
    except Exception as e:
        return f"Error summarizing text: {str(e)}"