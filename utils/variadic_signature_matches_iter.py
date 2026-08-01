
def variadic_signature_matches_iter(types, full_signature):
    """Check if a set of input types matches a variadic signature.

    Notes
    -----
    The algorithm is as follows:

    Initialize the current signature to the first in the sequence.
    For each type in ``types``:

    - If the current signature is variadic

      - If the type matches the signature, yield True
      - Else, try to get the next signature.
        If no signatures are left we can't possibly have a match,
        so yield False.

    - Else, yield True if the type matches the current signature.
      Get the next signature.
    """
    sigiter = iter(full_signature)
    sig = next(sigiter)
    for typ in types:
        matches = issubclass(typ, sig)
        yield matches
        if not isvariadic(sig):
            # we're not matching a variadic argument, so move to the next
            # element in the signature
            sig = next(sigiter)
    else:
        try:
            sig = next(sigiter)
        except StopIteration:
            if not isvariadic(sig):
                raise AssertionError("Expected variadic signature") from None
            yield True
        else:
            # We have signature items left over, so all of our arguments
            # haven't matched
            yield False

