
def simplify_index_permutations(expr, permutation_operators):
    """
    Performs simplification by introducing PermutationOperators where appropriate.

    Explanation
    ===========

    Schematically:
        [abij] - [abji] - [baij] + [baji] ->  P(ab)*P(ij)*[abij]

    permutation_operators is a list of PermutationOperators to consider.

    If permutation_operators=[P(ab),P(ij)] we will try to introduce the
    permutation operators P(ij) and P(ab) in the expression.  If there are other
    possible simplifications, we ignore them.

    >>> from sympy import symbols, Function
    >>> from sympy.physics.secondquant import simplify_index_permutations
    >>> from sympy.physics.secondquant import PermutationOperator
    >>> p,q,r,s = symbols('p,q,r,s')
    >>> f = Function('f')
    >>> g = Function('g')

    >>> expr = f(p)*g(q) - f(q)*g(p); expr
    f(p)*g(q) - f(q)*g(p)
    >>> simplify_index_permutations(expr,[PermutationOperator(p,q)])
    f(p)*g(q)*PermutationOperator(p, q)

    >>> PermutList = [PermutationOperator(p,q),PermutationOperator(r,s)]
    >>> expr = f(p,r)*g(q,s) - f(q,r)*g(p,s) + f(q,s)*g(p,r) - f(p,s)*g(q,r)
    >>> simplify_index_permutations(expr,PermutList)
    f(p, r)*g(q, s)*PermutationOperator(p, q)*PermutationOperator(r, s)

    """

    def _get_indices(expr, ind):
        """
        Collects indices recursively in predictable order.
        """
        result = []
        for arg in expr.args:
            if arg in ind:
                result.append(arg)
            else:
                if arg.args:
                    result.extend(_get_indices(arg, ind))
        return result

    def _choose_one_to_keep(a, b, ind):
        # we keep the one where indices in ind are in order ind[0] < ind[1]
        return min(a, b, key=lambda x: default_sort_key(_get_indices(x, ind)))

    expr = expr.expand()
    if isinstance(expr, Add):
        terms = set(expr.args)

        for P in permutation_operators:
            new_terms = set()
            on_hold = set()
            while terms:
                term = terms.pop()
                permuted = P.get_permuted(term)
                if permuted in terms | on_hold:
                    try:
                        terms.remove(permuted)
                    except KeyError:
                        on_hold.remove(permuted)
                    keep = _choose_one_to_keep(term, permuted, P.args)
                    new_terms.add(P*keep)
                else:

                    # Some terms must get a second chance because the permuted
                    # term may already have canonical dummy ordering.  Then
                    # substitute_dummies() does nothing.  However, the other
                    # term, if it exists, will be able to match with us.
                    permuted1 = permuted
                    permuted = substitute_dummies(permuted)
                    if permuted1 == permuted:
                        on_hold.add(term)
                    elif permuted in terms | on_hold:
                        try:
                            terms.remove(permuted)
                        except KeyError:
                            on_hold.remove(permuted)
                        keep = _choose_one_to_keep(term, permuted, P.args)
                        new_terms.add(P*keep)
                    else:
                        new_terms.add(term)
            terms = new_terms | on_hold
        return Add(*terms)
    return expr

