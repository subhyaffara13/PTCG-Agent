
def _annual_finder(vmin: float, vmax: float, freq: BaseOffset) -> np.ndarray:
    # Note: small difference here vs other finders in adding 1 to vmax
    (vmin, vmax) = (int(vmin), int(vmax + 1))
    span = vmax - vmin + 1

    info = np.zeros(
        span, dtype=[("val", int), ("maj", bool), ("min", bool), ("fmt", "|S8")]
    )
    info["val"] = np.arange(vmin, vmax + 1)
    info["fmt"] = ""
    dates_ = info["val"]

    (min_anndef, maj_anndef) = _get_default_annual_spacing(span)
    major_idx = dates_ % maj_anndef == 0
    minor_idx = dates_ % min_anndef == 0
    info["maj"][major_idx] = True
    info["min"][minor_idx] = True
    info["fmt"][major_idx] = "%Y"

    return info

