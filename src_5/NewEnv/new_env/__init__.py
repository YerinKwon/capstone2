from gym.envs.registration import register

register(
    id = 'env-v0',
    entry_point = 'new_env.envs:NewEnv',
)

register(
    id = 'env-ExtraHard-v0',
    entry_point = 'new_env.envs:NewEnvExtraHard',
)