
def _raise_incompatible_point(point, previous_point):
    raise ValueError(
        f"Quadratic splines must connect end-to-start; got {previous_point!r} then {point!r}"
    )

