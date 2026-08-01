
def _splitCubicAtTC(a, b, c, d, *ts):
    ts = list(ts)
    ts.insert(0, 0.0)
    ts.append(1.0)
    for i in range(len(ts) - 1):
        t1 = ts[i]
        t2 = ts[i + 1]
        delta = t2 - t1

        delta_2 = delta * delta
        delta_3 = delta * delta_2
        t1_2 = t1 * t1
        t1_3 = t1 * t1_2

        # calc new a, b, c and d
        a1 = a * delta_3
        b1 = (3 * a * t1 + b) * delta_2
        c1 = (2 * b * t1 + c + 3 * a * t1_2) * delta
        d1 = a * t1_3 + b * t1_2 + c * t1 + d
        pt1, pt2, pt3, pt4 = calcCubicPointsC(a1, b1, c1, d1)
        yield (pt1, pt2, pt3, pt4)

