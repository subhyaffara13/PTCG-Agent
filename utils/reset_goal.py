
def reset_goal(
    rng: chex.PRNGKey, available_goals: chex.Array, _: EnvParams
) -> chex.Array:
    """Reset the goal state/position in the environment."""
    goal_index = jax.random.randint(rng, (), 0, available_goals.shape[0])
    goal = available_goals[goal_index][:]
    return goal


def reset_goal(
    rng: chex.PRNGKey, available_goals: chex.Array, _: EnvParams
) -> chex.Array:
    """Reset the goal state/position in the environment."""
    goal_index = jax.random.randint(rng, (), 0, available_goals.shape[0])
    goal = available_goals[goal_index][:]
    return goal

