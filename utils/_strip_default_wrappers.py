
def _strip_default_wrappers(env: gym.Env) -> gym.Env:
    """Strips builtin wrappers from the environment.

    Args:
        env: the environment to strip builtin wrappers from

    Returns:
        The environment without builtin wrappers
    """
    default_wrappers = ()
    if hasattr(gym.wrappers, "render_collection"):
        default_wrappers += (gym.wrappers.render_collection.RenderCollection,)
    if hasattr(gym.wrappers, "human_rendering"):
        default_wrappers += (gym.wrappers.human_rendering.HumanRendering,)
    while isinstance(env, default_wrappers):
        env = env.env
    return env

