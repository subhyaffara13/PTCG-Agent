
def cc_rank(cc):
    r'''Rank the complexity score from A to F, where A stands for the simplest
    and best score and F the most complex and worst one:

    ============= =====================================================
        1 - 5        A (low risk - simple block)
        6 - 10       B (low risk - well structured and stable block)
        11 - 20      C (moderate risk - slightly complex block)
        21 - 30      D (more than moderate risk - more complex block)
        31 - 40      E (high risk - complex block, alarming)
        41+          F (very high risk - error-prone, unstable block)
    ============= =====================================================

    Here *block* is used in place of function, method or class.

    The formula used to convert the score into an index is the following:

    .. math::

        \text{rank} = \left \lceil \dfrac{\text{score}}{10} \right \rceil
        - H(5 - \text{score})

    where ``H(s)`` stands for the Heaviside Step Function.
    The rank is then associated to a letter (0 = A, 5 = F).
    '''
    if cc < 0:
        raise ValueError('Complexity must be a non-negative value')
    return chr(
        min(int(math.ceil(cc / 10.0) or 1) - (1, 0)[5 - cc < 0], 5) + 65
    )

