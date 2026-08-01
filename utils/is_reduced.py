
def is_reduced(G, ring):
    """
    Checks if G is a reduced Groebner basis.
    """
    order = ring.order
    domain = ring.domain

    G.sort(key=lambda g: order(g.LM))

    for i, g in enumerate(G):
        if g.LC != domain.one:
            return False

        for term in g.terms():
            for h in G[:i] + G[i + 1:]:
                if monomial_divides(h.LM, term[0]):
                    return False

    return True

