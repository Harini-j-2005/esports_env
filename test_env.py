from env.environment import EsportsEnv
from env.models import Action

env = EsportsEnv()

obs = env.reset()
print("Initial State:", obs)

for i in range(3):
    action = Action(command="focus_reaction")  # test action

    obs, reward, done, info = env.step(action)

    print(f"\nStep {i+1}")
    print("Observation:", obs)
    print("Reward:", reward)
    print("Done:", done)
    print("Error:", info)

    if done:
        break