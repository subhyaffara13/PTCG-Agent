
def _is_linelike(segment):
    maybeline = _alignment_transformation(segment).transformPoints(segment)
    return all(math.isclose(p[1], 0.0) for p in maybeline)

