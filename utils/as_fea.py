
def asFea(g):
    if hasattr(g, "asFea"):
        return g.asFea()
    elif isinstance(g, tuple) and len(g) == 2:
        return asFea(g[0]) + " - " + asFea(g[1])  # a range
    elif g.lower() in fea_keywords:
        return "\\" + g
    else:
        return g

