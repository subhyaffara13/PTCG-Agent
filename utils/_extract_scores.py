from typing import Any

def _extract_scores(env: Any) -> tuple[float, float, int]:
    """Return (score_p0, score_p1, winner) from a terminated env."""
    p0 = float(env.state[0].reward or 0.0)
    p1 = float(env.state[1].reward or 0.0)
    if p0 > p1:
        winner = 1
    elif p1 > p0:
        winner = -1
    else:
        winner = 0
    return p0, p1, winner

