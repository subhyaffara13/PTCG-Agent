
def _postprocess_state_mul(expr):
    """Transform a ``Mul`` of quantum expressions into canonical form.

    This function is registered ``_constructor_postprocessor_mapping`` as a
    transformer for ``Mul``. This means that every time a quantum expression
    is multiplied, this function will be called to transform it into canonical
    form as defined by the binary functions registered with
    ``_transform_state_pair``.

    The algorithm of this function is as follows. It walks the args
    of the input ``Mul`` from left to right and calls ``_transform_state_pair``
    on every overlapping pair of args. Each time ``_transform_state_pair``
    is called it can return a tuple of items or None. If None, the pair isn't
    transformed. If a tuple, then the last element of the tuple goes back into
    the args to be transformed again and the others are extended onto the result
    args list.

    The algorithm can be visualized in the following table:

    step   result                                 args
    ============================================================================
    #0     []                                     [a, b, c, d, e, f]
    #1     []                                     [T(a,b), c, d, e, f]
    #2     [T(a,b)[:-1]]                          [T(a,b)[-1], c, d, e, f]
    #3     [T(a,b)[:-1]]                          [T(T(a,b)[-1], c), d, e, f]
    #4     [T(a,b)[:-1], T(T(a,b)[-1], c)[:-1]]   [T(T(T(a,b)[-1], c)[-1], d), e, f]
    #5     ...

    One limitation of the current implementation is that we assume that only the
    last item of the transformed tuple goes back into the args to be transformed
    again. These seems to handle the cases needed for Mul. However, we may need
    to extend the algorithm to have the entire tuple go back into the args for
    further transformation.
    """
    args = list(expr.args)
    result = []

    # Continue as long as we have at least 2 elements
    while len(args) > 1:
        # Get first two elements
        first = args.pop(0)
        second = args[0]  # Look at second element without popping yet

        transformed = _transform_state_pair(first, second)

        if transformed is None:
            # If transform returns None, append first element
            result.append(first)
        else:
            # This item was transformed, pop and discard
            args.pop(0)
            # The last item goes back to be transformed again
            args.insert(0, transformed[-1])
            # All other items go directly into the result
            result.extend(transformed[:-1])

    # Append any remaining element
    if args:
        result.append(args[0])

    return Mul._from_args(result, is_commutative=False)

