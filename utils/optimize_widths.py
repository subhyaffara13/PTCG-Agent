
def optimizeWidths(widths):
    """Given a list of glyph widths, or dictionary mapping glyph width to number of
    glyphs having that, returns a tuple of best CFF default and nominal glyph widths.

    This algorithm is linear in UPEM+numGlyphs."""

    if not hasattr(widths, "items"):
        d = defaultdict(int)
        for w in widths:
            d[w] += 1
        widths = d

    keys = sorted(widths.keys())
    minw, maxw = keys[0], keys[-1]
    domain = list(range(minw, maxw + 1))

    # Cumulative sum/max forward/backward.
    cumFrqU = cumSum(widths, op=add)
    cumMaxU = cumSum(widths, op=max)
    cumFrqD = cumSum(widths, op=add, decreasing=True)
    cumMaxD = cumSum(widths, op=max, decreasing=True)

    # Cost per nominal choice, without default consideration.
    nomnCostU = missingdict(
        lambda x: cumFrqU[x] + cumFrqU[x - 108] + cumFrqU[x - 1132] * 3
    )
    nomnCostD = missingdict(
        lambda x: cumFrqD[x] + cumFrqD[x + 108] + cumFrqD[x + 1132] * 3
    )
    nomnCost = missingdict(lambda x: nomnCostU[x] + nomnCostD[x] - widths[x])

    # Cost-saving per nominal choice, by best default choice.
    dfltCostU = missingdict(
        lambda x: max(cumMaxU[x], cumMaxU[x - 108] * 2, cumMaxU[x - 1132] * 5)
    )
    dfltCostD = missingdict(
        lambda x: max(cumMaxD[x], cumMaxD[x + 108] * 2, cumMaxD[x + 1132] * 5)
    )
    dfltCost = missingdict(lambda x: max(dfltCostU[x], dfltCostD[x]))

    # Combined cost per nominal choice.
    bestCost = missingdict(lambda x: nomnCost[x] - dfltCost[x])

    # Best nominal.
    nominal = min(domain, key=lambda x: bestCost[x])

    # Work back the best default.
    bestC = bestCost[nominal]
    dfltC = nomnCost[nominal] - bestCost[nominal]
    ends = []
    if dfltC == dfltCostU[nominal]:
        starts = [nominal, nominal - 108, nominal - 1132]
        for start in starts:
            while cumMaxU[start] and cumMaxU[start] == cumMaxU[start - 1]:
                start -= 1
            ends.append(start)
    else:
        starts = [nominal, nominal + 108, nominal + 1132]
        for start in starts:
            while cumMaxD[start] and cumMaxD[start] == cumMaxD[start + 1]:
                start += 1
            ends.append(start)
    default = min(ends, key=lambda default: byteCost(widths, default, nominal))

    return default, nominal

