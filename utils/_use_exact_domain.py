
def _use_exact_domain(dom):
    """Check whether to convert to an exact domain."""
    # DomainMatrix can handle RR and CC with partial pivoting. Other inexact
    # domains like RR[a,b,...] can only be handled by converting to an exact
    # domain like QQ[a,b,...]
    if dom.is_RR or dom.is_CC:
        return False
    else:
        return not dom.is_Exact

