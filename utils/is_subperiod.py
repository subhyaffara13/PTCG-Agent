
def is_subperiod(source, target) -> bool:
    """
    Returns True if downsampling is possible between source and target
    frequencies

    Parameters
    ----------
    source : str or DateOffset
        Frequency converting from
    target : str or DateOffset
        Frequency converting to

    Returns
    -------
    bool
    """
    if target is None or source is None:
        return False
    source = _maybe_coerce_freq(source)
    target = _maybe_coerce_freq(target)

    if _is_annual(target):
        if _is_quarterly(source):
            return _quarter_months_conform(
                get_rule_month(source), get_rule_month(target)
            )
        return source in {"D", "C", "B", "M", "h", "min", "s", "ms", "us", "ns"}
    elif _is_quarterly(target):
        return source in {"D", "C", "B", "M", "h", "min", "s", "ms", "us", "ns"}
    elif _is_monthly(target):
        return source in {"D", "C", "B", "h", "min", "s", "ms", "us", "ns"}
    elif _is_weekly(target):
        return source in {target, "D", "C", "B", "h", "min", "s", "ms", "us", "ns"}
    elif target == "B":
        return source in {"B", "h", "min", "s", "ms", "us", "ns"}
    elif target == "C":
        return source in {"C", "h", "min", "s", "ms", "us", "ns"}
    elif target == "D":
        return source in {"D", "h", "min", "s", "ms", "us", "ns"}
    elif target == "h":
        return source in {"h", "min", "s", "ms", "us", "ns"}
    elif target == "min":
        return source in {"min", "s", "ms", "us", "ns"}
    elif target == "s":
        return source in {"s", "ms", "us", "ns"}
    elif target == "ms":
        return source in {"ms", "us", "ns"}
    elif target == "us":
        return source in {"us", "ns"}
    elif target == "ns":
        return source in {"ns"}
    else:
        return False

