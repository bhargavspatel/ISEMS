from openai import OpenAI
from app.core.config import OPENAI_API_KEY
from pydantic import BaseModel
import json


class AIRecommendationSchema(BaseModel):
    summary: str
    weakness_analysis: str
    recommended_actions: list[str]
    confidence_level: str


def rule_based_fallback(skill_name, mastery_score):
    if mastery_score < 0.5:
        return {
            "summary": f"Struggling in {skill_name}.",
            "weakness_analysis": "Fundamentals need improvement.",
            "recommended_actions": [
                "Review basic concepts.",
                "Solve beginner-level problems daily."
            ],
            "confidence_level": "low"
        }
    elif mastery_score < 0.75:
        return {
            "summary": f"Moderate understanding of {skill_name}.",
            "weakness_analysis": "Inconsistent performance detected.",
            "recommended_actions": [
                "Practice medium-level problems.",
                "Attempt timed quizzes."
            ],
            "confidence_level": "medium"
        }
    else:
        return {
            "summary": f"Strong mastery in {skill_name}.",
            "weakness_analysis": "No major weaknesses detected.",
            "recommended_actions": [
                "Attempt advanced challenges."
            ],
            "confidence_level": "high"
        }


def generate_ai_feedback(skill_name, mastery_score, recent_scores):
    # If no API key configured → fallback immediately
    if not OPENAI_API_KEY:
        return rule_based_fallback(skill_name, mastery_score)

    try:
        client = OpenAI(api_key=OPENAI_API_KEY)

        prompt = f"""
You are an educational performance analyst.

Student performance data:
Skill: {skill_name}
Mastery Score: {mastery_score}
Recent Scores: {recent_scores}

Return ONLY valid JSON in this format:
{{
  "summary": "...",
  "weakness_analysis": "...",
  "recommended_actions": ["...", "..."],
  "confidence_level": "low | medium | high"
}}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a structured JSON generator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )

        content = response.choices[0].message.content
        parsed = json.loads(content)
        validated = AIRecommendationSchema(**parsed)

        return validated.dict()

    except Exception as e:
        print("AI ERROR — Using fallback:", str(e))
        return rule_based_fallback(skill_name, mastery_score)