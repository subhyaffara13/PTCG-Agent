
def piecewiseLinearMap(v: float, mapping: Mapping[float, float]) -> float:
    keys = mapping.keys()
    if not keys:
        return v
    if v in keys:
        return mapping[v]
    k = min(keys)
    if v < k:
        return v + mapping[k] - k
    k = max(keys)
    if v > k:
        return v + mapping[k] - k
    # Interpolate
    a = max(k for k in keys if k < v)
    b = min(k for k in keys if k > v)
    va = mapping[a]
    vb = mapping[b]
    return va + (vb - va) * (v - a) / (b - a)

