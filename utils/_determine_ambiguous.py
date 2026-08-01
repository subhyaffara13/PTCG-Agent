
def _determine_ambiguous(term, ordered, ambiguous_groups):
    # We encountered a term for which the dummy substitution is ambiguous.
    # This happens for terms with 2 or more contractions between factors that
    # cannot be uniquely ordered independent of summation indices.  For
    # example:
    #
    # Sum(p, q) v^{p, .}_{q, .}v^{q, .}_{p, .}
    #
    # Assuming that the indices represented by . are dummies with the
    # same range, the factors cannot be ordered, and there is no
    # way to determine a consistent ordering of p and q.
    #
    # The strategy employed here, is to relabel all unambiguous dummies with
    # non-dummy symbols and call _get_ordered_dummies again.  This procedure is
    # applied to the entire term so there is a possibility that
    # _determine_ambiguous() is called again from a deeper recursion level.

    # break recursion if there are no ordered dummies
    all_ambiguous = set()
    for dummies in ambiguous_groups:
        all_ambiguous |= dummies
    all_ordered = set(ordered) - all_ambiguous
    if not all_ordered:
        # FIXME: If we arrive here, there are no ordered dummies. A method to
        # handle this needs to be implemented.  In order to return something
        # useful nevertheless, we choose arbitrarily the first dummy and
        # determine the rest from this one.  This method is dependent on the
        # actual dummy labels which violates an assumption for the
        # canonicalization procedure.  A better implementation is needed.
        group = [ d for d in ordered if d in ambiguous_groups[0] ]
        d = group[0]
        all_ordered.add(d)
        ambiguous_groups[0].remove(d)

    stored_counter = _symbol_factory._counter
    subslist = []
    for d in [ d for d in ordered if d in all_ordered ]:
        nondum = _symbol_factory._next()
        subslist.append((d, nondum))
    newterm = term.subs(subslist)
    neworder = _get_ordered_dummies(newterm)
    _symbol_factory._set_counter(stored_counter)

    # update ordered list with new information
    for group in ambiguous_groups:
        ordered_group = [ d for d in neworder if d in group ]
        ordered_group.reverse()
        result = []
        for d in ordered:
            if d in group:
                result.append(ordered_group.pop())
            else:
                result.append(d)
        ordered = result
    return ordered

