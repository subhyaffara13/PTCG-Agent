
def _register_bsuite_envs():
    """Registers all bsuite environments in gymnasium."""
    try:
        import bsuite
    except ImportError:
        return

    from bsuite.environments import Environment

    from shimmy.bsuite_compatibility import BSuiteCompatibilityV0

    # Add generic environment support
    def _make_bsuite_generic_env(env: Environment, render_mode: str):
        return BSuiteCompatibilityV0(env, render_mode=render_mode)

    register(
        "bsuite/compatibility-env-v0",
        _make_bsuite_generic_env,  # pyright: ignore[reportGeneralTypeIssues]
    )

    # register all prebuilt envs
    def _make_bsuite_env(env_id: str, **env_kwargs: Mapping[str, Any]):
        env = bsuite.load(env_id, env_kwargs)
        return BSuiteCompatibilityV0(env)

    # non deterministic envs
    nondeterministic = ["deep_sea", "bandit", "discounting_chain"]

    for env_id in BSUITE_ENVS:
        register(
            f"bsuite/{env_id}-v0",
            partial(_make_bsuite_env, env_id=env_id),
            nondeterministic=env_id in nondeterministic,
        )

