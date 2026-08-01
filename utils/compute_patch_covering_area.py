
def compute_patch_covering_area(left: int, upper: int, right: int, lower: int, side: int) -> float:
    w = right - left
    h = lower - upper
    w, h = max(w, h), min(w, h)
    if w > side:
        h = h / w * side
        w = side
    return w * h


def compute_patch_covering_area(left: int, upper: int, right: int, lower: int, side: int) -> float:
    w = right - left
    h = lower - upper
    w, h = max(w, h), min(w, h)
    if w > side:
        h = h / w * side
        w = side
    return w * h

