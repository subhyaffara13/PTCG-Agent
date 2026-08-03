import logging
import os
from typing import Any

def _default_formatter():
    fmt = os.environ.get(LOG_FORMAT_ENV_VAR, None)
    trace_id_filter = {
        item.strip()
        for item in os.environ.get(LOG_TRACE_ID_FILTER, "").split(",")
        if item.strip()
    }
    if fmt is None:
        return TorchLogsFormatter(trace_id_filter=trace_id_filter)
    else:
        if fmt in ("short", "basic"):
            fmt = logging.BASIC_FORMAT
        return logging.Formatter(fmt)


def _default_formatter(x: Any, precision: int, thousands: bool = False) -> Any:
    """
    Format the display of a value

    Parameters
    ----------
    x : Any
        Input variable to be formatted
    precision : Int
        Floating point precision used if ``x`` is float or complex.
    thousands : bool, default False
        Whether to group digits with thousands separated with ",".

    Returns
    -------
    value : Any
        Matches input type, or string if input is float or complex or int with sep.
    """
    if is_float(x) or is_complex(x):
        return f"{x:,.{precision}f}" if thousands else f"{x:.{precision}f}"
    elif is_integer(x):
        return f"{x:,}" if thousands else str(x)
    return x

