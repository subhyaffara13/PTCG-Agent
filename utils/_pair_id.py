
def _pair_id(row: dict) -> tuple:
    """Canonical pair id: unordered model pair + chance seed.

    Two seat-flipped games share this id (and share the same instance via
    the pinned chance seed). The permutation test shuffles labels at this
    granularity so seat-flip pairing is preserved.
    """
    a, b = sorted((row["model_p0"], row["model_p1"]))
    return (a, b, int(row["seed"]))

