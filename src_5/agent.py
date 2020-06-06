import tensorflow as tf
import numpy as np
import gym

from keras.models import Sequential, Model
from keras.layers import Dense, Activation, Flatten
from keras import Input
from keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.policy import EpsGreedyQPolicy
from rl.memory import SequentialMemory

def build_model(state_size, nb_actions):
    input = Input(shape=(1, state_size))
    x = Flatten()(input)
    x = Dense(16, activation='relu')(x)
    x = Dense(16, activation='relu')(x)
    output = Dense(nb_actions, activation='linear')(x)
    model = Model(inputs=input, outputs=output)

    return model

print('strt')
print(tf.__version__)

env = gym.make('new_env:env-v0')

nb_actions = env.action_space.n

model = Sequential()
#model.add(Flatten(input_shape=(1,) + env.observation_space.shape))
model.add(Dense(24, input_shape=(1,)))
model.add(Dense(12, activation='relu'))
model.add(Dense(12, activation='relu'))
model.add(Dense(nb_actions, activation='linear'))


print(model.summary())
print('after summary')
policy = EpsGreedyQPolicy()
memory = SequentialMemory(limit=50000, window_length=1)

dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=10, target_model_update=1e-2, policy=policy)
dqn.compile(Adam(lr=1e-3), metrics=['mae'])

dqn.fit(env, nb_steps=5000, visualize=True, verbose=0)

dqn.test(env, nb_episodes=5, visualize=True)
print('end')
