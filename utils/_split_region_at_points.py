
def _split_region_at_points(a, b, points, xp):
    """
    Given the integration limits `a` and `b` describing a rectangular region and a list
    of `points`, find the list of ``[(a_1, b_1), ..., (a_l, b_l)]`` which breaks up the
    initial region into smaller subregion such that no `points` lie strictly inside
    any of the subregions.
    """

    regions = [(a, b)]

    for point in points:
        if xp.any(xp.isinf(point)):
            # If a point is specified at infinity, ignore.
            #
            # This case occurs when points are given by the user to avoid, but after
            # applying a transformation, they are removed.
            continue

        new_subregions = []

        for a_k, b_k in regions:
            if _is_strictly_in_region(a_k, b_k, point, xp):
                subregions = _split_subregion(a_k, b_k, xp, point)

                for left, right in subregions:
                    # Skip any zero-width regions.
                    if xp.any(left == right):
                        continue
                    else:
                        new_subregions.append((left, right))

                new_subregions.extend(subregions)

            else:
                new_subregions.append((a_k, b_k))

        regions = new_subregions

    return regions

