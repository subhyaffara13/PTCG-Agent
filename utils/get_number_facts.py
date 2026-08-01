
def get_number_facts(x = None):
    """
    Facts between unary number predicates.

    Parameters
    ==========

    x : Symbol, optional
        Placeholder symbol for unary facts. Default is ``Symbol('x')``.

    Returns
    =======

    fact : Known facts in conjugated normal form.

    """
    if x is None:
        x = Symbol('x')

    fact = And(
        # primitive predicates for extended real exclude each other.
        Exclusive(Q.negative_infinite(x), Q.negative(x), Q.zero(x),
            Q.positive(x), Q.positive_infinite(x)),

        # build complex plane
        Exclusive(Q.real(x), Q.imaginary(x)),
        Implies(Q.real(x) | Q.imaginary(x), Q.complex(x)),

        # other subsets of complex
        Exclusive(Q.transcendental(x), Q.algebraic(x)),
        Equivalent(Q.real(x), Q.rational(x) | Q.irrational(x)),
        Exclusive(Q.irrational(x), Q.rational(x)),
        Implies(Q.rational(x), Q.algebraic(x)),

        # integers
        Exclusive(Q.even(x), Q.odd(x)),
        Implies(Q.integer(x), Q.rational(x)),
        Implies(Q.zero(x), Q.even(x)),
        Exclusive(Q.composite(x), Q.prime(x)),
        Implies(Q.composite(x) | Q.prime(x), Q.integer(x) & Q.positive(x)),
        Implies(Q.even(x) & Q.positive(x) & ~Q.prime(x), Q.composite(x)),

        # hermitian and antihermitian
        Implies(Q.real(x), Q.hermitian(x)),
        Implies(Q.imaginary(x), Q.antihermitian(x)),
        Implies(Q.zero(x), Q.hermitian(x) | Q.antihermitian(x)),

        # define finity and infinity, and build extended real line
        Exclusive(Q.infinite(x), Q.finite(x)),
        Implies(Q.complex(x), Q.finite(x)),
        Implies(Q.negative_infinite(x) | Q.positive_infinite(x), Q.infinite(x)),

        # commutativity
        Implies(Q.finite(x) | Q.infinite(x), Q.commutative(x)),
    )
    return fact

