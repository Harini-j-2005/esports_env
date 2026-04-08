def apply_training(player, action):
    reward = 0.0

    weakest = min(["aim", "reaction", "strategy"], key=lambda x: player[x])

    if action == f"focus_{weakest}":
        player[weakest] += 5
        reward += 0.5
    else:
        reward -= 0.2

    # fatigue increase
    player["fatigue"] += 3

    return player, reward