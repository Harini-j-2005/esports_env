def apply_analysis(player, action):
    reward = 0.0

    # simulate performance issue
    if player["fatigue"] > 30:
        issue = "high_fatigue"
    else:
        issue = "normal"

    if action == "analyze_performance":
        reward += 0.5

        # simulate improvement
        if issue == "high_fatigue":
            player["fatigue"] -= 5
            player["confidence"] += 3
            reward += 0.3
    else:
        reward -= 0.2

    return player, reward