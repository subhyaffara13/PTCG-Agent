
def _unify_with_other(self, other):
    """Unify self and other into a single matrix type, or check for scalar."""
    other, T = _coerce_operand(self, other)

    if T == "is_matrix":
        typ = classof(self, other)
        if typ != self.__class__:
            self = _convert_matrix(typ, self)
        if typ != other.__class__:
            other = _convert_matrix(typ, other)

    return self, other, T

