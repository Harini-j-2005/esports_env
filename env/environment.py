import random
from typing import Tuple, Dict, Any

from env.models import Observation, Action

from env.tasks.training_task import apply_training
from env.tasks.analysis_task import apply_analysis
from env.tasks.engagement_task import apply_engagement


class EsportsEnv:

    def __init__(self):
        self.state_data = {}
        self.task = None
        self.steps = 0
        self.done = False
        self.initial_state = None
        self.actions_taken = []

    def reset(self):
        self.steps = 0
        self.done = False
        self.actions_taken = []

        self.task = random.choice([
            "training",
            "analysis",
            "engagement"
        ])

        self.state_data = {
            "player": {
                "aim": 60,
                "reaction": 40,
                "strategy": 70,
                "fatigue": 20,
                "confidence": 50
            }
        }

        self.initial_state = {
            "player": self.state_data["player"].copy()
        }

        return Observation(
            task=self.task,
            state=self.state_data,
            step_count=self.steps
        )

    def step(self, action: Action) -> Tuple[Observation, float, bool, Dict]:

        self.steps += 1
        reward = 0.0
        error = None

        try:
            player = self.state_data["player"]
            action_cmd = action.command

            self.actions_taken.append(action_cmd)

            # TASK HANDLING
            if self.task == "training":
                player, reward = apply_training(player, action_cmd)

            elif self.task == "analysis":
                player, reward = apply_analysis(player, action_cmd)

            elif self.task == "engagement":
                player, reward = apply_engagement(player, action_cmd)

            # FATIGUE PENALTY
            if player["fatigue"] > 50:
                reward -= 0.3

            # END CONDITION
            if self.steps >= 3:
                self.done = True

        except Exception as e:
            error = str(e)
            reward -= 0.5

        return (
            Observation(
                task=self.task,
                state=self.state_data,
                step_count=self.steps
            ),
            round(reward, 2),
            self.done,
            {"error": error}
        )

    def state(self):
        return self.state_data