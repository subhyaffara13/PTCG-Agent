
def maybe_normalize(arg, parm):  # codespell:ignore
    """Normalize arg if a normalizer is registered."""
    normalizer = normalizers.get(parm.annotation)  # codespell:ignore
    return normalizer(arg, parm) if normalizer else arg  # codespell:ignore

