
def _beforeBuildPaintRadialGradient(paint, source):
    x0 = source["x0"]
    y0 = source["y0"]
    r0 = source["r0"]
    x1 = source["x1"]
    y1 = source["y1"]
    r1 = source["r1"]

    # TODO apparently no builder_test confirms this works (?)

    # avoid abrupt change after rounding when c0 is near c1's perimeter
    c = round_start_circle_stable_containment((x0, y0), r0, (x1, y1), r1)
    x0, y0 = c.centre
    r0 = c.radius

    # update source to ensure paint is built with corrected values
    source["x0"] = x0
    source["y0"] = y0
    source["r0"] = r0
    source["x1"] = x1
    source["y1"] = y1
    source["r1"] = r1

    return paint, source

