def calculate_mastery(submissions):

    if not submissions:
        return 0.0

    weights = [0.5, 0.3, 0.2]
    total = 0.0

    for i, submission in enumerate(submissions[:3]):
        ratio = submission.score / submission.assessment.max_score
        total += ratio * weights[i]

    return round(total, 2)

def generate_recommendation(skill_name, mastery_score):
    if mastery_score < 0.5:
        return f"You are struggling in {skill_name}. Focus on fundamentals and solve basic problems daily."
    elif mastery_score < 0.75:
        return f"You have moderate understanding of {skill_name}. Practice medium-level problems and timed quizzes."
    else:
        return f"You have strong mastery in {skill_name}. Try advanced challenges to deepen expertise."