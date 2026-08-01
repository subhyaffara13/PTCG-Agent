
def reidemeister_relators(C):
    R = C.fp_group.relators
    rels = [rewrite(C, coset, word) for word in R for coset in range(C.n)]
    order_1_gens = {i for i in rels if len(i) == 1}

    # remove all the order 1 generators from relators
    rels = list(filter(lambda rel: rel not in order_1_gens, rels))

    # replace order 1 generators by identity element in reidemeister relators
    for i in range(len(rels)):
        w = rels[i]
        w = w.eliminate_words(order_1_gens, _all=True)
        rels[i] = w

    C._schreier_generators = [i for i in C._schreier_generators
                    if not (i in order_1_gens or i**-1 in order_1_gens)]

    # Tietze transformation 1 i.e TT_1
    # remove cyclic conjugate elements from relators
    i = 0
    while i < len(rels):
        w = rels[i]
        j = i + 1
        while j < len(rels):
            if w.is_cyclic_conjugate(rels[j]):
                del rels[j]
            else:
                j += 1
        i += 1

    C._reidemeister_relators = rels

