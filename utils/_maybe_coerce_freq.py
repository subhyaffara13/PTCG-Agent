
def _maybe_coerce_freq(code) -> str:
    """we might need to coerce a code to a rule_code
    and uppercase it

    Parameters
    ----------
    source : str or DateOffset
        Frequency converting from

    Returns
    -------
    str
    """
    assert code is not None
    if isinstance(code, DateOffset):
        code = PeriodDtype(to_offset(code.name))._freqstr
    if code in {"h", "min", "s", "ms", "us", "ns"}:
        return code
    else:
        return code.upper()

