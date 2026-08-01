
def _compression_level_from_env() -> int:
    env_level = GPOS_COMPACT_MODE_DEFAULT
    if GPOS_COMPACT_MODE_ENV_KEY in os.environ:
        import warnings

        warnings.warn(
            f"'{GPOS_COMPACT_MODE_ENV_KEY}' environment variable is deprecated. "
            "Please set the 'fontTools.otlLib.optimize.gpos:COMPRESSION_LEVEL' option "
            "in TTFont.cfg.",
            DeprecationWarning,
        )

        env_level = os.environ[GPOS_COMPACT_MODE_ENV_KEY]
    if len(env_level) == 1 and env_level in "0123456789":
        return int(env_level)
    raise ValueError(f"Bad {GPOS_COMPACT_MODE_ENV_KEY}={env_level}")

