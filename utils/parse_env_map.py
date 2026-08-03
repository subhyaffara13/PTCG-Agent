from pathlib import Path


def parse_env_map(
    env: list[str] | None = None,
    env_file: str | None = None,
) -> dict[str, str | None]:
    """Parse ``-e``/``--env``/``-s``/``--secrets`` and ``--env-file``/``--secrets-file`` CLI args into a dict.

    Uses an extended environment that includes the user's HF token so that
    bare ``--secrets HF_TOKEN`` resolves correctly.
    """
    extended_environ = _get_extended_environ()
    env_map: dict[str, str | None] = {}
    if env_file:
        env_map.update(load_dotenv(Path(env_file).read_text(), environ=extended_environ))
    for env_value in env or []:
        env_map.update(load_dotenv(env_value, environ=extended_environ))
    return env_map

