
def _to_field(M):
    """Convert a DomainMatrix to a field if possible."""
    K = M.domain
    if K.has_assoc_Field:
        return M.to_field()
    else:
        return M

