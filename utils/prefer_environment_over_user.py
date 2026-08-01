
def prefer_environment_over_user() -> bool:
    """Determine if environment-level paths should take precedence over user-level paths."""
    # If JUPYTER_PREFER_ENV_PATH is defined, that signals user intent, so return its value
    if "JUPYTER_PREFER_ENV_PATH" in os.environ:
        return envset("JUPYTER_PREFER_ENV_PATH")

    # If we are in a Python virtualenv, default to True (see https://docs.python.org/3/library/venv.html#venv-def)
    if sys.prefix != sys.base_prefix and _do_i_own(sys.prefix):
        return True

    # If sys.prefix indicates Python comes from a conda/mamba environment that is not the root environment, default to True
    if (
        "CONDA_PREFIX" in os.environ
        and sys.prefix.startswith(os.environ["CONDA_PREFIX"])
        and os.environ.get("CONDA_DEFAULT_ENV", "base") != "base"
        and _do_i_own(sys.prefix)
    ):
        return True

    return False

