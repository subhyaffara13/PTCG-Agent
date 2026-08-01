
def test_gen(
    glyphsets,
    glyphs=None,
    names=None,
    ignore_missing=False,
    *,
    locations=None,
    tolerance=DEFAULT_TOLERANCE,
    kinkiness=DEFAULT_KINKINESS,
    upem=DEFAULT_UPEM,
    show_all=False,
    discrete_axes=[],
):
    if tolerance >= 10:
        tolerance *= 0.01
    assert 0 <= tolerance <= 1
    if kinkiness >= 10:
        kinkiness *= 0.01
    assert 0 <= kinkiness

    names = names or [repr(g) for g in glyphsets]

    if glyphs is None:
        # `glyphs = glyphsets[0].keys()` is faster, certainly, but doesn't allow for sparse TTFs/OTFs given out of order
        # ... risks the sparse master being the first one, and only processing a subset of the glyphs
        glyphs = {g for glyphset in glyphsets for g in glyphset.keys()}

    parents, order = find_parents_and_order(
        glyphsets, locations, discrete_axes=discrete_axes
    )

    def grand_parent(i, glyphname):
        if i is None:
            return None
        i = parents[i]
        if i is None:
            return None
        while parents[i] is not None and glyphsets[i][glyphname] is None:
            i = parents[i]
        return i

    for glyph_name in glyphs:
        log.info("Testing glyph %s", glyph_name)
        allGlyphs = [Glyph(glyph_name, glyphset) for glyphset in glyphsets]
        if len([1 for glyph in allGlyphs if not glyph.doesnt_exist]) <= 1:
            continue
        for master_idx, (glyph, glyphset, name) in enumerate(
            zip(allGlyphs, glyphsets, names)
        ):
            if glyph.doesnt_exist:
                if not ignore_missing:
                    yield (
                        glyph_name,
                        {
                            "type": InterpolatableProblem.MISSING,
                            "master": name,
                            "master_idx": master_idx,
                        },
                    )
                continue

            has_open = False
            for ix, open in enumerate(glyph.openContours):
                if not open:
                    continue
                has_open = True
                yield (
                    glyph_name,
                    {
                        "type": InterpolatableProblem.OPEN_PATH,
                        "master": name,
                        "master_idx": master_idx,
                        "contour": ix,
                    },
                )
            if has_open:
                continue

        matchings = [None] * len(glyphsets)

        for m1idx in order:
            glyph1 = allGlyphs[m1idx]
            if glyph1 is None or not glyph1.nodeTypes:
                continue
            m0idx = grand_parent(m1idx, glyph_name)
            if m0idx is None:
                continue
            glyph0 = allGlyphs[m0idx]
            if glyph0 is None or not glyph0.nodeTypes:
                continue

            #
            # Basic compatibility checks
            #

            m0 = glyph0.nodeTypes
            m1 = glyph1.nodeTypes
            if len(m0) != len(m1):
                yield (
                    glyph_name,
                    {
                        "type": InterpolatableProblem.PATH_COUNT,
                        "master_1": names[m0idx],
                        "master_2": names[m1idx],
                        "master_1_idx": m0idx,
                        "master_2_idx": m1idx,
                        "value_1": len(m0),
                        "value_2": len(m1),
                    },
                )
                continue

            if m0 != m1:
                for pathIx, (nodes1, nodes2) in enumerate(zip(m0, m1)):
                    if nodes1 == nodes2:
                        continue
                    if len(nodes1) != len(nodes2):
                        yield (
                            glyph_name,
                            {
                                "type": InterpolatableProblem.NODE_COUNT,
                                "path": pathIx,
                                "master_1": names[m0idx],
                                "master_2": names[m1idx],
                                "master_1_idx": m0idx,
                                "master_2_idx": m1idx,
                                "value_1": len(nodes1),
                                "value_2": len(nodes2),
                            },
                        )
                        continue
                    for nodeIx, (n1, n2) in enumerate(zip(nodes1, nodes2)):
                        if n1 != n2:
                            yield (
                                glyph_name,
                                {
                                    "type": InterpolatableProblem.NODE_INCOMPATIBILITY,
                                    "path": pathIx,
                                    "node": nodeIx,
                                    "master_1": names[m0idx],
                                    "master_2": names[m1idx],
                                    "master_1_idx": m0idx,
                                    "master_2_idx": m1idx,
                                    "value_1": n1,
                                    "value_2": n2,
                                },
                            )
                            continue

            #
            # InterpolatableProblem.CONTOUR_ORDER check
            #

            this_tolerance, matching = test_contour_order(glyph0, glyph1)
            if this_tolerance < tolerance:
                yield (
                    glyph_name,
                    {
                        "type": InterpolatableProblem.CONTOUR_ORDER,
                        "master_1": names[m0idx],
                        "master_2": names[m1idx],
                        "master_1_idx": m0idx,
                        "master_2_idx": m1idx,
                        "value_1": list(range(len(matching))),
                        "value_2": matching,
                        "tolerance": this_tolerance,
                    },
                )
                matchings[m1idx] = matching

            #
            # wrong-start-point / weight check
            #

            m0Isomorphisms = glyph0.isomorphisms
            m1Isomorphisms = glyph1.isomorphisms
            m0Vectors = glyph0.greenVectors
            m1Vectors = glyph1.greenVectors
            recording0 = glyph0.recordings
            recording1 = glyph1.recordings

            # If contour-order is wrong, adjust it
            matching = matchings[m1idx]
            if (
                matching is not None and m1Isomorphisms
            ):  # m1 is empty for composite glyphs
                m1Isomorphisms = [m1Isomorphisms[i] for i in matching]
                m1Vectors = [m1Vectors[i] for i in matching]
                recording1 = [recording1[i] for i in matching]

            midRecording = []
            for c0, c1 in zip(recording0, recording1):
                try:
                    r = RecordingPen()
                    r.value = list(lerpRecordings(c0.value, c1.value))
                    midRecording.append(r)
                except ValueError:
                    # Mismatch because of the reordering above
                    midRecording.append(None)

            for ix, (contour0, contour1) in enumerate(
                zip(m0Isomorphisms, m1Isomorphisms)
            ):
                if (
                    contour0 is None
                    or contour1 is None
                    or len(contour0) == 0
                    or len(contour0) != len(contour1)
                ):
                    # We already reported this; or nothing to do; or not compatible
                    # after reordering above.
                    continue

                this_tolerance, proposed_point, reverse = test_starting_point(
                    glyph0, glyph1, ix, tolerance, matching
                )

                if this_tolerance < tolerance:
                    yield (
                        glyph_name,
                        {
                            "type": InterpolatableProblem.WRONG_START_POINT,
                            "contour": ix,
                            "master_1": names[m0idx],
                            "master_2": names[m1idx],
                            "master_1_idx": m0idx,
                            "master_2_idx": m1idx,
                            "value_1": 0,
                            "value_2": proposed_point,
                            "reversed": reverse,
                            "tolerance": this_tolerance,
                        },
                    )

                # Weight check.
                #
                # If contour could be mid-interpolated, and the two
                # contours have the same area sign, proceeed.
                #
                # The sign difference can happen if it's a weirdo
                # self-intersecting contour; ignore it.
                contour = midRecording[ix]

                if contour and (m0Vectors[ix][0] < 0) == (m1Vectors[ix][0] < 0):
                    midStats = StatisticsPen(glyphset=None)
                    contour.replay(midStats)

                    midVector = contour_vector_from_stats(midStats)

                    m0Vec = m0Vectors[ix]
                    m1Vec = m1Vectors[ix]
                    size0 = m0Vec[0] * m0Vec[0]
                    size1 = m1Vec[0] * m1Vec[0]
                    midSize = midVector[0] * midVector[0]

                    for overweight, problem_type in enumerate(
                        (
                            InterpolatableProblem.UNDERWEIGHT,
                            InterpolatableProblem.OVERWEIGHT,
                        )
                    ):
                        if overweight:
                            expectedSize = max(size0, size1)
                            continue  # disabled
                        else:
                            expectedSize = sqrt(size0 * size1)

                        log.debug(
                            "%s: actual size %g; threshold size %g, master sizes: %g, %g",
                            problem_type,
                            midSize,
                            expectedSize,
                            size0,
                            size1,
                        )

                        if (
                            not overweight and expectedSize * tolerance > midSize + 1e-5
                        ) or (overweight and 1e-5 + expectedSize / tolerance < midSize):
                            try:
                                if overweight:
                                    this_tolerance = expectedSize / midSize
                                else:
                                    this_tolerance = midSize / expectedSize
                            except ZeroDivisionError:
                                this_tolerance = 0
                            log.debug("tolerance %g", this_tolerance)
                            yield (
                                glyph_name,
                                {
                                    "type": problem_type,
                                    "contour": ix,
                                    "master_1": names[m0idx],
                                    "master_2": names[m1idx],
                                    "master_1_idx": m0idx,
                                    "master_2_idx": m1idx,
                                    "tolerance": this_tolerance,
                                },
                            )

            #
            # "kink" detector
            #
            m0 = glyph0.points
            m1 = glyph1.points

            # If contour-order is wrong, adjust it
            if matchings[m1idx] is not None and m1:  # m1 is empty for composite glyphs
                m1 = [m1[i] for i in matchings[m1idx]]

            t = 0.1  # ~sin(radian(6)) for tolerance 0.95
            deviation_threshold = (
                upem * DEFAULT_KINKINESS_LENGTH * DEFAULT_KINKINESS / kinkiness
            )

            for ix, (contour0, contour1) in enumerate(zip(m0, m1)):
                if (
                    contour0 is None
                    or contour1 is None
                    or len(contour0) == 0
                    or len(contour0) != len(contour1)
                ):
                    # We already reported this; or nothing to do; or not compatible
                    # after reordering above.
                    continue

                # Walk the contour, keeping track of three consecutive points, with
                # middle one being an on-curve. If the three are co-linear then
                # check for kinky-ness.
                for i in range(len(contour0)):
                    pt0 = contour0[i]
                    pt1 = contour1[i]
                    if not pt0[1] or not pt1[1]:
                        # Skip off-curves
                        continue
                    pt0_prev = contour0[i - 1]
                    pt1_prev = contour1[i - 1]
                    pt0_next = contour0[(i + 1) % len(contour0)]
                    pt1_next = contour1[(i + 1) % len(contour1)]

                    if pt0_prev[1] and pt1_prev[1]:
                        # At least one off-curve is required
                        continue
                    if pt0_next[1] and pt1_next[1]:
                        # At least one off-curve is required
                        continue

                    pt0 = complex(*pt0[0])
                    pt1 = complex(*pt1[0])
                    pt0_prev = complex(*pt0_prev[0])
                    pt1_prev = complex(*pt1_prev[0])
                    pt0_next = complex(*pt0_next[0])
                    pt1_next = complex(*pt1_next[0])

                    # We have three consecutive points. Check whether
                    # they are colinear.
                    d0_prev = pt0 - pt0_prev
                    d0_next = pt0_next - pt0
                    d1_prev = pt1 - pt1_prev
                    d1_next = pt1_next - pt1

                    sin0 = d0_prev.real * d0_next.imag - d0_prev.imag * d0_next.real
                    sin1 = d1_prev.real * d1_next.imag - d1_prev.imag * d1_next.real
                    try:
                        sin0 /= abs(d0_prev) * abs(d0_next)
                        sin1 /= abs(d1_prev) * abs(d1_next)
                    except ZeroDivisionError:
                        continue

                    if abs(sin0) > t or abs(sin1) > t:
                        # Not colinear / not smooth.
                        continue

                    # Check the mid-point is actually, well, in the middle.
                    dot0 = d0_prev.real * d0_next.real + d0_prev.imag * d0_next.imag
                    dot1 = d1_prev.real * d1_next.real + d1_prev.imag * d1_next.imag
                    if dot0 < 0 or dot1 < 0:
                        # Sharp corner.
                        continue

                    # Fine, if handle ratios are similar...
                    r0 = abs(d0_prev) / (abs(d0_prev) + abs(d0_next))
                    r1 = abs(d1_prev) / (abs(d1_prev) + abs(d1_next))
                    r_diff = abs(r0 - r1)
                    if abs(r_diff) < t:
                        # Smooth enough.
                        continue

                    mid = (pt0 + pt1) / 2
                    mid_prev = (pt0_prev + pt1_prev) / 2
                    mid_next = (pt0_next + pt1_next) / 2

                    mid_d0 = mid - mid_prev
                    mid_d1 = mid_next - mid

                    sin_mid = mid_d0.real * mid_d1.imag - mid_d0.imag * mid_d1.real
                    try:
                        sin_mid /= abs(mid_d0) * abs(mid_d1)
                    except ZeroDivisionError:
                        continue

                    # ...or if the angles are similar.
                    if abs(sin_mid) * (tolerance * kinkiness) <= t:
                        # Smooth enough.
                        continue

                    # How visible is the kink?

                    cross = sin_mid * abs(mid_d0) * abs(mid_d1)
                    arc_len = abs(mid_d0 + mid_d1)
                    deviation = abs(cross / arc_len)
                    if deviation < deviation_threshold:
                        continue
                    deviation_ratio = deviation / arc_len
                    if deviation_ratio > t:
                        continue

                    this_tolerance = t / (abs(sin_mid) * kinkiness)

                    log.debug(
                        "kink: deviation %g; deviation_ratio %g; sin_mid %g; r_diff %g",
                        deviation,
                        deviation_ratio,
                        sin_mid,
                        r_diff,
                    )
                    log.debug("tolerance %g", this_tolerance)
                    yield (
                        glyph_name,
                        {
                            "type": InterpolatableProblem.KINK,
                            "contour": ix,
                            "master_1": names[m0idx],
                            "master_2": names[m1idx],
                            "master_1_idx": m0idx,
                            "master_2_idx": m1idx,
                            "value": i,
                            "tolerance": this_tolerance,
                        },
                    )

            #
            # --show-all
            #

            if show_all:
                yield (
                    glyph_name,
                    {
                        "type": InterpolatableProblem.NOTHING,
                        "master_1": names[m0idx],
                        "master_2": names[m1idx],
                        "master_1_idx": m0idx,
                        "master_2_idx": m1idx,
                    },
                )

