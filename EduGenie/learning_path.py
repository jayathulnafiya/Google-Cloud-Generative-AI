from config import generate_text

def get_learning_recommendations(topic: str) -> str:
    try:
        prompt = (
            f"Generate a personalized, structured learning path for the topic: '{topic}'. "
            f"Include beginner to advanced concepts, organized by difficulty, "
            f"supported with useful resource suggestions (videos, articles, books) and step-by-step guidance."
        )
        return generate_text(prompt)
    except Exception as e:
        return f"Error generating learning path: {str(e)}"