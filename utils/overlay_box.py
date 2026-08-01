
def overlayBox(top, bot):
    """Overlays ``top`` box on top of ``bot`` box.

    Returns two items:

    * Box for intersection of ``top`` and ``bot``, or None if they don't intersect.
    * Box for remainder of ``bot``.  Remainder box might not be exact (since the
      remainder might not be a simple box), but is inclusive of the exact
      remainder.
    """

    # Intersection
    intersection = {}
    intersection.update(top)
    intersection.update(bot)
    for axisTag in set(top) & set(bot):
        min1, max1 = top[axisTag]
        min2, max2 = bot[axisTag]
        minimum = max(min1, min2)
        maximum = min(max1, max2)
        if not minimum < maximum:
            return None, bot  # Do not intersect
        intersection[axisTag] = minimum, maximum

    # Remainder
    #
    # Remainder is empty if bot's each axis range lies within that of intersection.
    #
    # Remainder is shrank if bot's each, except for exactly one, axis range lies
    # within that of intersection, and that one axis, it extrudes out of the
    # intersection only on one side.
    #
    # Bot is returned in full as remainder otherwise, as true remainder is not
    # representable as a single box.

    remainder = dict(bot)
    extruding = False
    fullyInside = True
    for axisTag in top:
        if axisTag in bot:
            continue
        extruding = True
        fullyInside = False
        break
    for axisTag in bot:
        if axisTag not in top:
            continue  # Axis range lies fully within
        min1, max1 = intersection[axisTag]
        min2, max2 = bot[axisTag]
        if min1 <= min2 and max2 <= max1:
            continue  # Axis range lies fully within

        # Bot's range doesn't fully lie within that of top's for this axis.
        # We know they intersect, so it cannot lie fully without either; so they
        # overlap.

        # If we have had an overlapping axis before, remainder is not
        # representable as a box, so return full bottom and go home.
        if extruding:
            return intersection, bot
        extruding = True
        fullyInside = False

        # Otherwise, cut remainder on this axis and continue.
        if min1 <= min2:
            # Right side survives.
            minimum = max(max1, min2)
            maximum = max2
        elif max2 <= max1:
            # Left side survives.
            minimum = min2
            maximum = min(min1, max2)
        else:
            # Remainder leaks out from both sides.  Can't cut either.
            return intersection, bot

        remainder[axisTag] = minimum, maximum

    if fullyInside:
        # bot is fully within intersection.  Remainder is empty.
        return intersection, None

    return intersection, remainder

