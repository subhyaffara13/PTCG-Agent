
def optimizeWidthsBruteforce(widths):
    """Bruteforce version.  Veeeeeeeeeeeeeeeeery slow.  Only works for smallests of fonts."""

    d = defaultdict(int)
    for w in widths:
        d[w] += 1

    # Maximum number of bytes using default can possibly save
    maxDefaultAdvantage = 5 * max(d.values())

    minw, maxw = min(widths), max(widths)
    domain = list(range(minw, maxw + 1))

    bestCostWithoutDefault = min(byteCost(widths, None, nominal) for nominal in domain)

    bestCost = len(widths) * 5 + 1
    for nominal in domain:
        if byteCost(widths, None, nominal) > bestCost + maxDefaultAdvantage:
            continue
        for default in domain:
            cost = byteCost(widths, default, nominal)
            if cost < bestCost:
                bestCost = cost
                bestDefault = default
                bestNominal = nominal

    return bestDefault, bestNominal

