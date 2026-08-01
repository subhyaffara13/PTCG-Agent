
def _check_engine(engine: str | None) -> str:
    """
    Make sure a valid engine is passed.

    Parameters
    ----------
    engine : str
        String to validate.

    Raises
    ------
    KeyError
      * If an invalid engine is passed.
    ImportError
      * If numexpr was requested but doesn't exist.

    Returns
    -------
    str
        Engine name.
    """
    from pandas.core.computation.check import NUMEXPR_INSTALLED
    from pandas.core.computation.expressions import USE_NUMEXPR

    if engine is None:
        engine = "numexpr" if USE_NUMEXPR else "python"

    if engine not in ENGINES:
        valid_engines = list(ENGINES.keys())
        raise KeyError(
            f"Invalid engine '{engine}' passed, valid engines are {valid_engines}"
        )

    # TODO: validate this in a more general way (thinking of future engines
    # that won't necessarily be import-able)
    # Could potentially be done on engine instantiation
    if engine == "numexpr" and not NUMEXPR_INSTALLED:
        raise ImportError(
            "'numexpr' is not installed or an unsupported version. Cannot use "
            "engine='numexpr' for query/eval if 'numexpr' is not installed"
        )

    return engine

