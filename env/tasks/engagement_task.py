def apply_engagement(player, action):
    reward = 0.0

    # simulate fan trust / confidence impact
    if action == "engage_fans_positive":
        player["confidence"] += 5
        reward += 1.0

    elif action == "ignore_toxic":
        player["confidence"] += 2
        reward += 0.5

    else:
        player["confidence"] -= 3
        reward -= 0.3

    return player, reward