def grade_training(initial_state, final_state):
    initial = initial_state["player"]
    final = final_state["player"]

    improvement = (
        (final["aim"] - initial["aim"]) +
        (final["reaction"] - initial["reaction"]) +
        (final["strategy"] - initial["strategy"])
    )

    score = improvement / 15  # max possible improvement

    return max(0.0, min(1.0, score))