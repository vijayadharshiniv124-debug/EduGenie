from gemini_client import generate_json

PATH_SCHEMA = {
    "type": "object",
    "properties": {
        "topic": {"type": "string"},
        "level": {"type": "string"},
        "goal": {"type": "string"},
        "steps": {"type": "array", "items": {"type": "string"}, "minItems": 4, "maxItems": 8},
        "practice_ideas": {"type": "array", "items": {"type": "string"}, "minItems": 2, "maxItems": 5},
        "next_level": {"type": "string"},
    },
    "required": ["topic", "level", "goal", "steps", "practice_ideas", "next_level"],
}


def recommend_learning_path(topic: str, level: str = "beginner"):
    topic = topic.strip()
    level = level.strip()
    if not topic:
        raise ValueError("Please provide a learning topic.")
    prompt = (
        f"Create a personalized learning path for the topic '{topic}' at the '{level}' level. "
        "Move logically from fundamentals toward advanced material. Include a goal, ordered study steps, practical "
        "practice ideas, and the next level the learner should reach. Keep it realistic for a student."
    )
    return generate_json(prompt, PATH_SCHEMA)
