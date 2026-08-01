
def load_results(
    base: str | Path, pylint_home: str | Path = PYLINT_HOME
) -> LinterStats | None:
    base = Path(base)
    pylint_home = Path(pylint_home)
    data_file = _get_pdata_path(base, 1, pylint_home)

    if not data_file.exists():
        return None

    try:
        with open(data_file, "rb") as stream:
            data = pickle.load(stream)
            if not isinstance(data, LinterStats):
                warnings.warn(
                    "You're using an old pylint cache with invalid data following "
                    f"an upgrade, please delete '{data_file}'.",
                    UserWarning,
                    stacklevel=2,
                )
                raise TypeError
            return data
    except Exception:  # pylint: disable=broad-except
        # There's an issue with the cache but we just continue as if it isn't there
        return None

