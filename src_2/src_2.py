from tensorforce.agents import Agent
from tensorforce.execution import Runner
from tensorforce.environments import Environment
from capstone2.src_2.agent import agent_rl

environment = Environment.create(environment = 'environment.json', max_episode_timesteps= 200)
agent = Agent.create(agent = agent_rl, environment = environment)

# Train
for _ in range(200):
    states = environment.reset()
    terminal = False
    while not terminal:
        actions = agent.act(states = states)
        states, terminal, reward = environment.execute(actions = actions)
        agent.observe(terminal = terminal, reward = reward)

# Evaluate

sum_rewards = 0.0
for _ in range(100):
    states = environment.reset()
    internals = agent.initial_internals()
    terminal = False
    while not terminal:
        actions, internals = agent.act(states = states, internals = internals, evaluation = True)
        states, terminal, reward = environment.execute(action = actions)
        sum_rewards += reward



agent.close()
environment.close()




