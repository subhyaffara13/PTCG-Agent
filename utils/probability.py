
def probability(value: float):
    """Ensures that `value` is a valid probability number, i.e. [0,1]."""
    if not 0 <= value <= 1:
        raise ValueError(f"Value must be a probability between 0.0 and 1.0, got {value}.")


def probability(condition, given_condition=None, numsamples=None,
                evaluate=True, **kwargs):
    """
    Probability that a condition is true, optionally given a second condition.

    Parameters
    ==========

    condition : Combination of Relationals containing RandomSymbols
        The condition of which you want to compute the probability
    given_condition : Combination of Relationals containing RandomSymbols
        A conditional expression. P(X > 1, X > 0) is expectation of X > 1
        given X > 0
    numsamples : int
        Enables sampling and approximates the probability with this many samples
    evaluate : Bool (defaults to True)
        In case of continuous systems return unevaluated integral

    Examples
    ========

    >>> from sympy.stats import P, Die
    >>> from sympy import Eq
    >>> X, Y = Die('X', 6), Die('Y', 6)
    >>> P(X > 3)
    1/2
    >>> P(Eq(X, 5), X > 2) # Probability that X == 5 given that X > 2
    1/4
    >>> P(X > Y)
    5/12
    """

    kwargs['numsamples'] = numsamples
    from sympy.stats.symbolic_probability import Probability
    if evaluate:
        return Probability(condition, given_condition).doit(**kwargs)
    return Probability(condition, given_condition)

