
def single_ellipsis_index(names, fn_name):
    ellipsis_indices = [i for i, name in enumerate(names) if is_ellipsis(name)]
    if len(ellipsis_indices) >= 2:
        raise RuntimeError(
            f"{fn_name}: More than one Ellipsis ('...') found in names ("
            f"{names}). This function supports up to one Ellipsis."
        )
    if len(ellipsis_indices) == 1:
        return ellipsis_indices[0]
    return None

