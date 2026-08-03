from pathlib import Path


def _yield_default_files() -> Iterator[Path]:
    """Iterate over the default config file names and see if they exist."""
    for config_name in CONFIG_NAMES:
        try:
            if config_name.is_file():
                if config_name.suffix == ".toml" and not _toml_has_config(config_name):
                    continue
                if config_name.suffix in {
                    ".cfg",
                    ".ini",
                } and not _cfg_or_ini_has_config(config_name):
                    continue

                yield config_name.resolve()
        except OSError:
            pass

