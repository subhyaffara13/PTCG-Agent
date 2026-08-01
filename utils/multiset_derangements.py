
def multiset_derangements(s):
    """Generate derangements of the elements of s *in place*.

    Examples
    ========

    >>> from sympy.utilities.iterables import multiset_derangements, uniq

    Because the derangements of multisets (not sets) are generated
    in place, copies of the return value must be made if a collection
    of derangements is desired or else all values will be the same:

    >>> list(uniq([i for i in multiset_derangements('1233')]))
    [[None, None, None, None]]
    >>> [i.copy() for i in multiset_derangements('1233')]
    [['3', '3', '1', '2'], ['3', '3', '2', '1']]
    >>> [''.join(i) for i in multiset_derangements('1233')]
    ['3312', '3321']
    """
    from sympy.core.sorting import ordered
    # create multiset dictionary of hashable elements or else
    # remap elements to integers
    try:
        ms = multiset(s)
    except TypeError:
        # give each element a canonical integer value
        key = dict(enumerate(ordered(uniq(s))))
        h = []
        for si in s:
            for k in key:
                if key[k] == si:
                    h.append(k)
                    break
        for i in multiset_derangements(h):
            yield [key[j] for j in i]
        return

    mx = max(ms.values())  # max repetition of any element
    n = len(s)  # the number of elements

    ## special cases

    # 1) one element has more than half the total cardinality of s: no
    # derangements are possible.
    if mx*2 > n:
        return

    # 2) all elements appear once: singletons
    if len(ms) == n:
        yield from _set_derangements(s)
        return

    # find the first element that is repeated the most to place
    # in the following two special cases where the selection
    # is unambiguous: either there are two elements with multiplicity
    # of mx or else there is only one with multiplicity mx
    for M in ms:
        if ms[M] == mx:
            break

    inonM = [i for i in range(n) if s[i] != M]  # location of non-M
    iM = [i for i in range(n) if s[i] == M]  # locations of M
    rv = [None]*n

    # 3) half are the same
    if 2*mx == n:
        # M goes into non-M locations
        for i in inonM:
            rv[i] = M
        # permutations of non-M go to M locations
        for p in multiset_permutations([s[i] for i in inonM]):
            for i, pi in zip(iM, p):
                rv[i] = pi
            yield rv
        # clean-up (and encourages proper use of routine)
        rv[:] = [None]*n
        return

    # 4) single repeat covers all but 1 of the non-repeats:
    # if there is one repeat then the multiset of the values
    # of ms would be {mx: 1, 1: n - mx}, i.e. there would
    # be n - mx + 1 values with the condition that n - 2*mx = 1
    if n - 2*mx == 1 and len(ms.values()) == n - mx + 1:
        for i, i1 in enumerate(inonM):
            ifill = inonM[:i] + inonM[i+1:]
            for j in ifill:
                rv[j] = M
            for p in permutations([s[j] for j in ifill]):
                rv[i1] = s[i1]
                for j, pi in zip(iM, p):
                    rv[j] = pi
                k = i1
                for j in iM:
                    rv[j], rv[k] = rv[k], rv[j]
                    yield rv
                    k = j
        # clean-up (and encourages proper use of routine)
        rv[:] = [None]*n
        return

    ## general case is handled with 3 helpers:
    #    1) `finish_derangements` will place the last two elements
    #       which have arbitrary multiplicities, e.g. for multiset
    #       {c: 3, a: 2, b: 2}, the last two elements are a and b
    #    2) `iopen` will tell where a given element can be placed
    #    3) `do` will recursively place elements into subsets of
    #        valid locations

    def finish_derangements():
        """Place the last two elements into the partially completed
        derangement, and yield the results.
        """

        a = take[1][0]  # penultimate element
        a_ct = take[1][1]
        b = take[0][0]  # last element to be placed
        b_ct = take[0][1]

        # split the indexes of the not-already-assigned elements of rv into
        # three categories
        forced_a = []  # positions which must have an a
        forced_b = []  # positions which must have a b
        open_free = []  # positions which could take either
        for i in range(len(s)):
            if rv[i] is None:
                if s[i] == a:
                    forced_b.append(i)
                elif s[i] == b:
                    forced_a.append(i)
                else:
                    open_free.append(i)

        if len(forced_a) > a_ct or len(forced_b) > b_ct:
            # No derangement possible
            return

        for i in forced_a:
            rv[i] = a
        for i in forced_b:
            rv[i] = b
        for a_place in combinations(open_free, a_ct - len(forced_a)):
            for a_pos in a_place:
                rv[a_pos] = a
            for i in open_free:
                if rv[i] is None:  # anything not in the subset is set to b
                    rv[i] = b
            yield rv
            # Clean up/undo the final placements
            for i in open_free:
                rv[i] = None

        # additional cleanup - clear forced_a, forced_b
        for i in forced_a:
            rv[i] = None
        for i in forced_b:
            rv[i] = None

    def iopen(v):
        # return indices at which element v can be placed in rv:
        # locations which are not already occupied if that location
        # does not already contain v in the same location of s
        return [i for i in range(n) if rv[i] is None and s[i] != v]

    def do(j):
        if j == 1:
            # handle the last two elements (regardless of multiplicity)
            # with a special method
            yield from finish_derangements()
        else:
            # place the mx elements of M into a subset of places
            # into which it can be replaced
            M, mx = take[j]
            for i in combinations(iopen(M), mx):
                # place M
                for ii in i:
                    rv[ii] = M
                # recursively place the next element
                yield from do(j - 1)
                # mark positions where M was placed as once again
                # open for placement of other elements
                for ii in i:
                    rv[ii] = None

    # process elements in order of canonically decreasing multiplicity
    take = sorted(ms.items(), key=lambda x:(x[1], x[0]))
    yield from do(len(take) - 1)
    rv[:] = [None]*n

