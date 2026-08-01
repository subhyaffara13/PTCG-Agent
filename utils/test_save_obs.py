
def test_save_obs(env):
    env.reset()
    try:
        check_save_obs(env)
        for agent in env.agents:
            save_observation(env=env, agent=agent, save_dir="saved_observations")

    except AssertionError as ae:
        print("did not save the observations: ", ae)

