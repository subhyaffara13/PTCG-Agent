
def test_observation_action_spaces(env, agent_0):
    for agent in env.agents:
        assert isinstance(
            env.observation_space(agent), gymnasium.spaces.Space
        ), "Observation space for each agent must extend gymnasium.spaces.Space"
        assert isinstance(
            env.action_space(agent), gymnasium.spaces.Space
        ), "Agent space for each agent must extend gymnasium.spaces.Space"
        assert env.observation_space(agent) is env.observation_space(agent), (
            "observation_space should return the exact same space object (not a copy) for an agent (ensures that observation space seeding works as expected). "
            "Consider decorating your observation_space(self, agent) method with @functools.lru_cache(maxsize=None) to enable caching, or changing it to read from a dict such as self.observation_spaces."
        )
        assert env.action_space(agent) is env.action_space(agent), (
            "action_space should return the exact same space object (not a copy) for an agent (ensures that action space seeding works as expected). "
            "Consider decorating your action_space(self, agent) method with @functools.lru_cache(maxsize=None) to enable caching, or changing it to read from a dict such as self.action_spaces."
        )
        if (
            not (
                isinstance(env.observation_space(agent), gymnasium.spaces.Box)
                or isinstance(env.observation_space(agent), gymnasium.spaces.Discrete)
            )
            and str(env.unwrapped) not in env_obs_space
        ):
            warnings.warn(
                "Observation space for each agent probably should be gymnasium.spaces.box or gymnasium.spaces.discrete"
            )
        if not (
            isinstance(env.action_space(agent), gymnasium.spaces.Box)
            or isinstance(env.action_space(agent), gymnasium.spaces.Discrete)
        ):
            warnings.warn(
                "Action space for each agent probably should be gymnasium.spaces.box or gymnasium.spaces.discrete"
            )
        if (not isinstance(agent, str)) and agent != "env":
            warnings.warn(
                "Agents are recommended to have numbered string names, like player_0"
            )
        if not isinstance(agent, str) or not re.match(
            "[a-z]+_[0-9]+", agent
        ):  # regex for ending in _<integer>
            warnings.warn(
                'We recommend agents to be named in the format <descriptor>_<number>, like "player_0"'
            )
        if not isinstance(
            env.observation_space(agent), env.observation_space(agent_0).__class__
        ):
            warnings.warn(
                "The class of observation spaces is different between two agents"
            )
        if not isinstance(env.action_space(agent), env.action_space(agent).__class__):
            warnings.warn("The class of action spaces is different between two agents")
        if (
            env.observation_space(agent) != env.observation_space(agent_0)
            and str(env.unwrapped) not in env_diff_agent_obs_size
        ):
            warnings.warn("Agents have different observation space sizes")
        if env.action_space(agent) != env.action_space(agent):
            warnings.warn("Agents have different action space sizes")

        if isinstance(env.action_space(agent), gymnasium.spaces.Box):
            if np.any(np.equal(env.action_space(agent).low, -np.inf)):
                warnings.warn(
                    "Agent's minimum action space value is -infinity. This is probably too low."
                )
            if np.any(np.equal(env.action_space(agent).high, np.inf)):
                warnings.warn(
                    "Agent's maximum action space value is infinity. This is probably too high"
                )
            if np.any(
                np.equal(env.action_space(agent).low, env.action_space(agent).high)
            ):
                warnings.warn(
                    "Agent's maximum and minimum action space values are equal"
                )
            if np.any(
                np.greater(env.action_space(agent).low, env.action_space(agent).high)
            ):
                assert (
                    False
                ), "Agent's minimum action space value is greater than it's maximum"
            if env.action_space(agent).low.shape != env.action_space(agent).shape:
                assert (
                    False
                ), "Agent's action_space.low and action_space have different shapes"
            if env.action_space(agent).high.shape != env.action_space(agent).shape:
                assert (
                    False
                ), "Agent's action_space.high and action_space have different shapes"

        if isinstance(env.observation_space(agent), gymnasium.spaces.Box):
            if (
                np.any(np.equal(env.observation_space(agent).low, -np.inf))
                and str(env.unwrapped) not in env_neg_inf_obs
            ):
                warnings.warn(
                    "Agent's minimum observation space value is -infinity. This is probably too low."
                )
            if (
                np.any(np.equal(env.observation_space(agent).high, np.inf))
                and str(env.unwrapped) not in env_pos_inf_obs
            ):
                warnings.warn(
                    "Agent's maximum observation space value is infinity. This is probably too high"
                )
            if np.any(
                np.equal(
                    env.observation_space(agent).low, env.observation_space(agent).high
                )
            ):
                warnings.warn(
                    "Agent's maximum and minimum observation space values are equal"
                )
            if np.any(
                np.greater(
                    env.observation_space(agent).low, env.observation_space(agent).high
                )
            ):
                assert (
                    False
                ), "Agent's minimum observation space value is greater than it's maximum"
            if (
                env.observation_space(agent).low.shape
                != env.observation_space(agent).shape
            ):
                assert (
                    False
                ), "Agent's observation_space.low and observation_space have different shapes"
            if (
                env.observation_space(agent).high.shape
                != env.observation_space(agent).shape
            ):
                assert (
                    False
                ), "Agent's observation_space.high and observation_space have different shapes"

