
def elimination_technique_2(C):
    """
    This technique eliminates one generator at a time. Heuristically this
    seems superior in that we may select for elimination the generator with
    shortest equivalent string at each stage.

    >>> from sympy.combinatorics import free_group
    >>> from sympy.combinatorics.fp_groups import FpGroup, coset_enumeration_r, \
            reidemeister_relators, define_schreier_generators, elimination_technique_2
    >>> F, x, y = free_group("x, y")
    >>> f = FpGroup(F, [x**3, y**5, (x*y)**2]); H = [x*y, x**-1*y**-1*x*y*x]
    >>> C = coset_enumeration_r(f, H)
    >>> C.compress(); C.standardize()
    >>> define_schreier_generators(C)
    >>> reidemeister_relators(C)
    >>> elimination_technique_2(C)
    ([y_1, y_2], [y_2**-3, y_2*y_1*y_2*y_1*y_2*y_1, y_1**2])

    """
    rels = C._reidemeister_relators
    rels.sort(reverse=True)
    gens = C._schreier_generators
    for i in range(len(gens) - 1, -1, -1):
        rel = rels[i]
        for j in range(len(gens) - 1, -1, -1):
            gen = gens[j]
            if rel.generator_count(gen) == 1:
                k = rel.exponent_sum(gen)
                gen_index = rel.index(gen**k)
                bk = rel.subword(gen_index + 1, len(rel))
                fw = rel.subword(0, gen_index)
                rep_by = (bk*fw)**(-1*k)
                del rels[i]
                del gens[j]
                rels = [rel.eliminate_word(gen, rep_by) for rel in rels]
                break
    C._reidemeister_relators = rels
    C._schreier_generators = gens
    return C._schreier_generators, C._reidemeister_relators

