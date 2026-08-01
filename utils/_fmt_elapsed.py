
def _fmt_elapsed(secs: float) -> str:
    if secs < 60:
        return f"{int(secs):2d}s"
    return f"{int(secs // 60):2d}m{int(secs % 60):02d}s"

