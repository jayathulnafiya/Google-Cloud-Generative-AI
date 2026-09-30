from config import generate_text

def get_explanation(topic: str) -> str:
    try:
        prompt = f"Provide a simple, beginner-friendly, concise explanation of the concept: '{topic}'. Break down complex topics into easily understandable language."
        return generate_text(prompt)
    except Exception as e:
        return f"Error generating explanation: {str(e)}"