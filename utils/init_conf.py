
def init_conf(profile: Optional[str] = None) -> Dict[str, Any]:
    """
    Loads config JSON from:
      1) $AICORE_CONFIG if set, otherwise
      2) $AICORE_HOME/config.json (or config_<profile>.json when profile is given/not default)
    Returns {} when nothing is found.
    """
    home = Path(_get_home())
    profile = profile or os.environ.get(PROFILE_ENV_VAR)
    cfg_env = os.getenv(CONFIG_FILE_ENV_VAR)
    cfg_path = (
        Path(cfg_env)
        if cfg_env
        else (
            home
            / (
                "config.json"
                if profile in (None, "", "default")
                else f"config_{profile}.json"
            )
        )
    )

    if cfg_path and cfg_path.exists():
        try:
            with cfg_path.open(encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            raise KeyError(f"{cfg_path} is not valid JSON. Please fix or remove it!")

    # If an explicit non-default profile was requested but not found, raise.
    if cfg_env or (profile not in (None, "", "default")):
        raise FileNotFoundError(
            f"Unable to locate profile config file at '{cfg_path}' in AICORE_HOME '{home}'"
        )

    return {}

