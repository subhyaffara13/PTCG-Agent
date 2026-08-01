
def lch_to_husl(triple):
    L, C, H = triple

    if L > 99.9999999:
        return [H, 0.0, 100.0]
    if L < 0.00000001:
        return [H, 0.0, 0.0]

    mx = max_chroma(L, H)
    S = C / mx * 100.0

    return [H, S, L]

