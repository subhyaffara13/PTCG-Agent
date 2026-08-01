
def save_observation(
    env: AECEnv[AgentID, Any, Any],
    agent: AgentID | None = None,
    all_agents: bool = False,
    save_dir: str = os.getcwd(),
) -> None:
    from PIL import Image

    if agent is None:
        agent = env.agent_selection
    agent_list = [agent]
    if all_agents:
        agent_list = env.agents[:]
    for a in agent_list:
        _check_observation_saveable(env, a)
        save_folder = "{}/{}".format(
            save_dir, str(env).replace("<", "_").replace(">", "_")
        )
        os.makedirs(save_folder, exist_ok=True)

        # Parallel envs don't have observe method
        observation = env.observe(a)
        assert (
            observation is not None
        ), "Observation must be different than None to save as an image"
        rescaled = observation.astype(np.uint8)
        im = Image.fromarray(rescaled)
        fname = os.path.join(save_folder, str(a) + ".png")
        im.save(fname)

