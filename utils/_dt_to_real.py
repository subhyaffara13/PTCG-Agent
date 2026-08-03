from typing import Any

def _dt_to_real(dt: torch.dtype | Any) -> torch.dtype | Any:
    if not isinstance(dt, torch.dtype):
        return dt

    return COMPLEX_TO_REAL[dt]

