
def halstead_visitor_report(visitor):
    """Return a HalsteadReport from a HalsteadVisitor instance."""
    h1, h2 = visitor.distinct_operators, visitor.distinct_operands
    N1, N2 = visitor.operators, visitor.operands
    h = h1 + h2
    N = N1 + N2
    if h1 and h2:
        length = h1 * math.log(h1, 2) + h2 * math.log(h2, 2)
    else:
        length = 0
    volume = N * math.log(h, 2) if h != 0 else 0
    difficulty = (h1 * N2) / float(2 * h2) if h2 != 0 else 0
    effort = difficulty * volume
    return HalsteadReport(
        h1,
        h2,
        N1,
        N2,
        h,
        N,
        length,
        volume,
        difficulty,
        effort,
        effort / 18.0,
        volume / 3000.0,
    )

