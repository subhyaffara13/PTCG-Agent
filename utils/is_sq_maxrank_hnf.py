
def is_sq_maxrank_HNF(dm):
    r"""
    Say whether a :py:class:`~.DomainMatrix` is in that special case of Hermite
    Normal Form, in which the matrix is also square and of maximal rank.

    Explanation
    ===========

    We commonly work with :py:class:`~.Submodule` instances whose matrix is in
    this form, and it can be useful to be able to check that this condition is
    satisfied.

    For example this is the case with the :py:class:`~.Submodule` ``ZK``
    returned by :py:func:`~sympy.polys.numberfields.basis.round_two`, which
    represents the maximal order in a number field, and with ideals formed
    therefrom, such as ``2 * ZK``.

    """
    if dm.domain.is_ZZ and dm.is_square and dm.is_upper:
        n = dm.shape[0]
        for i in range(n):
            d = dm[i, i].element
            if d <= 0:
                return False
            for j in range(i + 1, n):
                if not (0 <= dm[i, j].element < d):
                    return False
        return True
    return False

