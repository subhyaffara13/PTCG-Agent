
def _simplify_relators(rels):
    """
    Simplifies a set of relators. All relators are checked to see if they are
    of the form `gen^n`. If any such relators are found then all other relators
    are processed for strings in the `gen` known order.

    Examples
    ========

    >>> from sympy.combinatorics import free_group
    >>> from sympy.combinatorics.fp_groups import _simplify_relators
    >>> F, x, y = free_group("x, y")
    >>> w1 = [x**2*y**4, x**3]
    >>> _simplify_relators(w1)
    [x**3, x**-1*y**4]

    >>> w2 = [x**2*y**-4*x**5, x**3, x**2*y**8, y**5]
    >>> _simplify_relators(w2)
    [x**-1*y**-2, x**-1*y*x**-1, x**3, y**5]

    >>> w3 = [x**6*y**4, x**4]
    >>> _simplify_relators(w3)
    [x**4, x**2*y**4]

    >>> w4 = [x**2, x**5, y**3]
    >>> _simplify_relators(w4)
    [x, y**3]

    """
    rels = rels[:]

    if not rels:
        return []

    identity = rels[0].group.identity

    # build dictionary with "gen: n" where gen^n is one of the relators
    exps = {}
    for i in range(len(rels)):
        rel = rels[i]
        if rel.number_syllables() == 1:
            g = rel[0]
            exp = abs(rel.array_form[0][1])
            if rel.array_form[0][1] < 0:
                rels[i] = rels[i]**-1
                g = g**-1
            if g in exps:
                exp = gcd(exp, exps[g].array_form[0][1])
            exps[g] = g**exp

    one_syllables_words = list(exps.values())
    # decrease some of the exponents in relators, making use of the single
    # syllable relators
    for i, rel in enumerate(rels):
        if rel in one_syllables_words:
            continue
        rel = rel.eliminate_words(one_syllables_words, _all = True)
        # if rels[i] contains g**n where abs(n) is greater than half of the power p
        # of g in exps, g**n can be replaced by g**(n-p) (or g**(p-n) if n<0)
        for g in rel.contains_generators():
            if g in exps:
                exp = exps[g].array_form[0][1]
                max_exp = (exp + 1)//2
                rel = rel.eliminate_word(g**(max_exp), g**(max_exp-exp), _all = True)
                rel = rel.eliminate_word(g**(-max_exp), g**(-(max_exp-exp)), _all = True)
        rels[i] = rel

    rels = [r.identity_cyclic_reduction() for r in rels]

    rels += one_syllables_words # include one_syllable_words in the list of relators
    rels = list(set(rels)) # get unique values in rels
    rels.sort()

    # remove <identity> entries in rels
    try:
        rels.remove(identity)
    except ValueError:
        pass
    return rels

