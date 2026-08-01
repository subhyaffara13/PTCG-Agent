
def _to_DM(A, ans):
    if isinstance(A, DomainMatrix):
        return A
    elif isinstance(A, Matrix):
        return A.to_DM(ans.domain)
    return DomainMatrix(A.to_list(), A.shape, A.domain)


def _to_DM(A, ans):
    """Convert the answer to DomainMatrix."""
    if isinstance(A, DomainMatrix):
        return A.to_dense()
    elif isinstance(A, DDM):
        return DomainMatrix(list(A), A.shape, A.domain).to_dense()
    elif isinstance(A, SDM):
        return DomainMatrix(dict(A), A.shape, A.domain).to_dense()
    else:
        assert False # pragma: no cover


def _to_DM(A, ans):
    """Convert the answer to DomainMatrix."""
    if isinstance(A, DomainMatrix):
        return A.to_dense()
    elif isinstance(A, Matrix):
        return A.to_DM(ans.domain).to_dense()

    if not (hasattr(A, 'shape') and hasattr(A, 'domain')):
        shape, domain = ans.shape, ans.domain
    else:
        shape, domain = A.shape, A.domain

    if isinstance(A, (DDM, list)):
        return DomainMatrix(list(A), shape, domain).to_dense()
    elif isinstance(A, (SDM, dict)):
        return DomainMatrix(dict(A), shape, domain).to_dense()
    else:
        assert False # pragma: no cover

