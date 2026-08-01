
def select_unit(t: float) -> tuple[str, float]:
    """Determine how to scale times for O(1) magnitude.

    This utility is used to format numbers for human consumption.
    """
    time_unit = {-3: "ns", -2: "us", -1: "ms"}.get(int(torch.tensor(t).log10().item() // 3), "s")
    time_scale = {"ns": 1e-9, "us": 1e-6, "ms": 1e-3, "s": 1}[time_unit]
    return time_unit, time_scale

