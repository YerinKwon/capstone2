import rlglue.RLGlue
from rlglue import RLGlue
from rlglue.agent.Agent import Agent
from rlglue.agent import AgentLoader as AgentLoader
from rlglue.types import Action
from rlglue.utils import TaskSpecVRLGLUE3

import RL_core.agent
import RL_core.env


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

Agt_rf = agent_rf(host)
Env_rf = env_rf(host)
localGlueImplementation_rf = LocalGlue(Env_rf, Agt_rf)

rl_rf = RLGlue()
rl_rf.setGlue(localGlueImplementation_rf)

rl_rf.RL_init()
rl_rf.RL_start()




def update():
    rl_rf.RL_step()