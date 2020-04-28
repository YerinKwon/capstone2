from rlglue.agent.Agent import Agent
from rlglue.agent import AgentLoader as AgentLoader
from rlglue.types import Action
from rlglue.utils import TaskSpecVRLGLUE3
"""
environment = Environment.create(
    environment = 'environment.json'
)
agent = Agent.create(agent = 'agent.json', environment = environment)

for _ in range():
    states = environment.reset()
    terminal = False
    while not terminal:
        actions = agent.act(states = states)
        states, terminal, reward = environment.execute(actions = actions)
        agent.observe(terminal = terminal, reward = reward)

sum_rewards = 0.0
for _ in range():
    states = environment.reset()
    internals = agent.initial_internals()
    terminal = False
    while not terminal:
        actions, internals = agent.act(states = states, internals = internals, evaluation = True)
        states, terminal, reward = environment.execute(actions = actions)
        sum_rewards += reward

agent.close()
environment.close()"""