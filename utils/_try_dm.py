
def _try_DM(M, use_EX=False):
    """Try to convert a matrix to a ``DomainMatrix``."""
    dM = M.to_DM()
    K = dM.domain

    # Return DomainMatrix if a domain is found. Only use EX if use_EX=True.
    if not use_EX and K.is_EXRAW:
        return None
    elif K.is_EXRAW:
        return dM.convert_to(EX)
    else:
        return dM

