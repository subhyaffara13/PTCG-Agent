
def _switch_domain(g, K):
    # An algebraic relation f(a, b) = 0 over Q can also be written
    # g(b) = 0 where g is in Q(a)[x] and h(a) = 0 where h is in Q(b)[x].
    # This function transforms g into h where Q(b) = K.
    frep = g.rep.inject()
    hrep = frep.eject(K, front=True)

    return g.new(hrep, g.gens[0])

