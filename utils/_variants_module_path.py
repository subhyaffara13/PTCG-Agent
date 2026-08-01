
def _variants_module_path(env_name: str) -> str:
    """Map env name to the dotted path of its ``prompt_variants`` module."""
    if env_name.startswith("open_spiel_"):
        game = env_name[len("open_spiel_") :]
        return f"kaggle_environments.envs.open_spiel_env.games.{game}.prompt_variants"
    return f"kaggle_environments.envs.{env_name}.prompt_variants"

