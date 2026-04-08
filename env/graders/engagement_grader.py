def grade_engagement(initial_state, final_state):
    initial = initial_state["player"]
    final = final_state["player"]

    confidence_gain = final["confidence"] - initial["confidence"]

    score = confidence_gain / 10

    return max(0.0, min(1.0, score))