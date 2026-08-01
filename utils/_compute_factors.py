
def _compute_factors(roots, multiplicity, include_powers=False):
    """Compute the total polynomial divided by factors for each root."""
    current = np.array([1])
    suffixes = [current]
    for pole, mult in zip(roots[-1:0:-1], multiplicity[-1:0:-1]):
        monomial = np.array([1, -pole])
        for _ in range(mult):
            current = np.polymul(current, monomial)
        suffixes.append(current)
    suffixes = suffixes[::-1]

    factors = []
    current = np.array([1])
    for pole, mult, suffix in zip(roots, multiplicity, suffixes):
        monomial = np.array([1, -pole])
        block = []
        for i in range(mult):
            if i == 0 or include_powers:
                block.append(np.polymul(current, suffix))
            current = np.polymul(current, monomial)
        factors.extend(reversed(block))

    return factors, current

