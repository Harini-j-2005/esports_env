def grade_analysis(actions_taken):
    correct = 0

    for action in actions_taken:
        if action == "analyze_performance":
            correct += 1

    score = correct / len(actions_taken)

    return max(0.0, min(1.0, score))