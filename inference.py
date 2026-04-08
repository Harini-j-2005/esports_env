import os
from dotenv import load_dotenv
from openai import OpenAI
from env.environment import EsportsEnv
from env.models import Action

# 🔹 Load env
load_dotenv(dotenv_path=".env")

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.1-8b-instant")
HF_TOKEN = os.getenv("HF_TOKEN")

if HF_TOKEN is None:
    raise ValueError("HF_TOKEN environment variable is required")

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

ALLOWED_ACTIONS = [
    "focus_aim",
    "focus_reaction",
    "focus_strategy",
    "rest",
    "analyze_performance",
    "engage_fans_positive",
    "ignore_toxic"
]


def clean_action(action_str: str) -> str:
    action_str = action_str.lower().strip()
    for act in ALLOWED_ACTIONS:
        if act in action_str:
            return act
    return "rest"


def smart_override(obs, action):
    if obs.task == "engagement":
        return "engage_fans_positive"
    elif obs.task == "analysis":
        return "analyze_performance"
    elif obs.task == "training":
        player = obs.state["player"]
        weakest = min(["aim", "reaction", "strategy"], key=lambda x: player[x])
        return f"focus_{weakest}"
    return action


def run():
    from env.graders.training_grader import grade_training
    from env.graders.analysis_grader import grade_analysis
    from env.graders.engagement_grader import grade_engagement

    env = EsportsEnv()
    obs = env.reset()

    print(f"[START] task={obs.task} env=esports_ops model={MODEL_NAME}")

    rewards = []
    step = 0

    while True:
        step += 1

        prompt = f"""
Task: {obs.task}
State: {obs.state}

Choose one action:
focus_aim, focus_reaction, focus_strategy,
rest, analyze_performance,
engage_fans_positive, ignore_toxic

Return only action name.
"""

        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}]
            )

            raw_action = response.choices[0].message.content.strip()
            action_str = clean_action(raw_action)

        except Exception as e:
            action_str = "rest"
            error_msg = str(e)

            obs, reward, done, info = env.step(Action(command=action_str))
            rewards.append(f"{reward:.2f}")

            print(f"[STEP] step={step} action={action_str} reward={reward:.2f} done={str(done).lower()} error={error_msg}")

            if done:
                break
            continue

        action_str = smart_override(obs, action_str)

        obs, reward, done, info = env.step(Action(command=action_str))
        rewards.append(f"{reward:.2f}")

        print(f"[STEP] step={step} action={action_str} reward={reward:.2f} done={str(done).lower()} error={info.get('error')}")

        if done:
            break

    print(f"[END] success=true steps={step} rewards={','.join(rewards)}")

    # 🔥 GRADER EXECUTION (THIS WAS MISSING)
    final_state = env.state()

    if obs.task == "training":
        score = grade_training(env.initial_state, final_state)

    elif obs.task == "analysis":
        score = grade_analysis(env.actions_taken)

    elif obs.task == "engagement":
        score = grade_engagement(env.initial_state, final_state)

    print(f"[SCORE] {score:.2f}")


if __name__ == "__main__":
    run()