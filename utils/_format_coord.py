
def _format_coord(freq: BaseOffset, t, y) -> str:
    time_period = Period(ordinal=int(t), freq=freq)
    return f"t = {time_period}  y = {y:8f}"

