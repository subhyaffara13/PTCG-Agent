
def multiset_partitions_taocp(multiplicities):
    """Enumerates partitions of a multiset.

    Parameters
    ==========

    multiplicities
         list of integer multiplicities of the components of the multiset.

    Yields
    ======

    state
        Internal data structure which encodes a particular partition.
        This output is then usually processed by a visitor function
        which combines the information from this data structure with
        the components themselves to produce an actual partition.

        Unless they wish to create their own visitor function, users will
        have little need to look inside this data structure.  But, for
        reference, it is a 3-element list with components:

        f
            is a frame array, which is used to divide pstack into parts.

        lpart
            points to the base of the topmost part.

        pstack
            is an array of PartComponent objects.

        The ``state`` output offers a peek into the internal data
        structures of the enumeration function.  The client should
        treat this as read-only; any modification of the data
        structure will cause unpredictable (and almost certainly
        incorrect) results.  Also, the components of ``state`` are
        modified in place at each iteration.  Hence, the visitor must
        be called at each loop iteration.  Accumulating the ``state``
        instances and processing them later will not work.

    Examples
    ========

    >>> from sympy.utilities.enumerative import list_visitor
    >>> from sympy.utilities.enumerative import multiset_partitions_taocp
    >>> # variables components and multiplicities represent the multiset 'abb'
    >>> components = 'ab'
    >>> multiplicities = [1, 2]
    >>> states = multiset_partitions_taocp(multiplicities)
    >>> list(list_visitor(state, components) for state in states)
    [[['a', 'b', 'b']],
    [['a', 'b'], ['b']],
    [['a'], ['b', 'b']],
    [['a'], ['b'], ['b']]]

    See Also
    ========

    sympy.utilities.iterables.multiset_partitions: Takes a multiset
        as input and directly yields multiset partitions.  It
        dispatches to a number of functions, including this one, for
        implementation.  Most users will find it more convenient to
        use than multiset_partitions_taocp.

    """

    # Important variables.
    # m is the number of components, i.e., number of distinct elements
    m = len(multiplicities)
    # n is the cardinality, total number of elements whether or not distinct
    n = sum(multiplicities)

    # The main data structure, f segments pstack into parts.  See
    # list_visitor() for example code indicating how this internal
    # state corresponds to a partition.

    # Note: allocation of space for stack is conservative.  Knuth's
    # exercise 7.2.1.5.68 gives some indication of how to tighten this
    # bound, but this is not implemented.
    pstack = [PartComponent() for i in range(n * m + 1)]
    f = [0] * (n + 1)

    # Step M1 in Knuth (Initialize)
    # Initial state - entire multiset in one part.
    for j in range(m):
        ps = pstack[j]
        ps.c = j
        ps.u = multiplicities[j]
        ps.v = multiplicities[j]

    # Other variables
    f[0] = 0
    a = 0
    lpart = 0
    f[1] = m
    b = m  # in general, current stack frame is from a to b - 1

    while True:
        while True:
            # Step M2 (Subtract v from u)
            k = b
            x = False
            for j in range(a, b):
                pstack[k].u = pstack[j].u - pstack[j].v
                if pstack[k].u == 0:
                    x = True
                elif not x:
                    pstack[k].c = pstack[j].c
                    pstack[k].v = min(pstack[j].v, pstack[k].u)
                    x = pstack[k].u < pstack[j].v
                    k = k + 1
                else:  # x is True
                    pstack[k].c = pstack[j].c
                    pstack[k].v = pstack[k].u
                    k = k + 1
                # Note: x is True iff v has changed

            # Step M3 (Push if nonzero.)
            if k > b:
                a = b
                b = k
                lpart = lpart + 1
                f[lpart + 1] = b
                # Return to M2
            else:
                break  # Continue to M4

        # M4  Visit a partition
        state = [f, lpart, pstack]
        yield state

        # M5 (Decrease v)
        while True:
            j = b-1
            while (pstack[j].v == 0):
                j = j - 1
            if j == a and pstack[j].v == 1:
                # M6 (Backtrack)
                if lpart == 0:
                    return
                lpart = lpart - 1
                b = a
                a = f[lpart]
                # Return to M5
            else:
                pstack[j].v = pstack[j].v - 1
                for k in range(j + 1, b):
                    pstack[k].v = pstack[k].u
                break  # GOTO M2

