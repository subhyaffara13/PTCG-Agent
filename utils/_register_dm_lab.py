from typing import Any

def _register_dm_lab():
    try:
        import deepmind_lab
    except ImportError:
        return

    from shimmy.dm_lab_compatibility import DmLabCompatibilityV0

    def _make_dm_lab_env(
        env_id: str, observations, config: dict[str, Any], renderer: str
    ):
        env = deepmind_lab.Lab(env_id, observations, config=config, renderer=renderer)
        return DmLabCompatibilityV0(env)

    register(
        id="DmLabCompatibility-v0",
        entry_point=_make_dm_lab_env,  # pyright: ignore[reportGeneralTypeIssues]
    )

