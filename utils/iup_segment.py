
def iup_segment(
    coords: _PointSegment, rc1: _Point, rd1: _Delta, rc2: _Point, rd2: _Delta
):  # -> _DeltaSegment:
    """Given two reference coordinates `rc1` & `rc2` and their respective
    delta vectors `rd1` & `rd2`, returns interpolated deltas for the set of
    coordinates `coords`."""

    # rc1 = reference coord 1
    # rd1 = reference delta 1
    out_arrays = [None, None]
    for j in 0, 1:
        out_arrays[j] = out = []
        x1, x2, d1, d2 = rc1[j], rc2[j], rd1[j], rd2[j]

        if x1 == x2:
            n = len(coords)
            if d1 == d2:
                out.extend([d1] * n)
            else:
                out.extend([0] * n)
            continue

        if x1 > x2:
            x1, x2 = x2, x1
            d1, d2 = d2, d1

        # x1 < x2
        scale = (d2 - d1) / (x2 - x1)
        for pair in coords:
            x = pair[j]

            if x <= x1:
                d = d1
            elif x >= x2:
                d = d2
            else:
                # Interpolate
                #
                # NOTE: we assign an explicit intermediate variable here in
                # order to disable a fused mul-add optimization. See:
                #
                # - https://godbolt.org/z/YsP4T3TqK,
                # - https://github.com/fonttools/fonttools/issues/3703
                nudge = (x - x1) * scale
                d = d1 + nudge

            out.append(d)

    return zip(*out_arrays)

