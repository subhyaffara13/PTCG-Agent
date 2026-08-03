from typing import Any

def get_arith_intensity(data: Any) -> float:
    m = data["m"]
    k = data["k"]
    n = data["n"]
    if m == 0 or k == 0 or n == 0:
        return 0.0
    return m * k * n / (m * k + k * n + m * n)

