
def _resolve_seed(env):
    """Resolve the episode seed from env.info / configuration, then scrub.

    Mirrors crawl/kaggriculture/orbit_wars: read env.info["seed"] first (the
    harness may have set it), then configuration.seed, then fall back to a
    random value. Clear configuration.seed so agents can't read it, and stash
    the resolved value on env.info["seed"] so it persists into the replay.
    """
    if not hasattr(env, "info") or env.info is None:
        env.info = {}
    seed = env.info.get("seed")
    if seed is None:
        seed = getattr(env.configuration, "seed", None)
    if seed is None:
        seed = random.randrange(2**31)
    try:
        env.configuration.seed = None
    except (AttributeError, TypeError):
        env.configuration["seed"] = None
    env.info["seed"] = seed
    return seed

