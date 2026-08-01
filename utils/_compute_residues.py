
def _compute_residues(poles, multiplicity, numerator):
    denominator_factors, _ = _compute_factors(poles, multiplicity)
    numerator = numerator.astype(poles.dtype)

    residues = []
    for pole, mult, factor in zip(poles, multiplicity,
                                  denominator_factors):
        if mult == 1:
            residues.append(np.polyval(numerator, pole) /
                            np.polyval(factor, pole))
        else:
            numer = numerator.copy()
            monomial = np.array([1, -pole])
            factor, d = np.polydiv(factor, monomial)

            block = []
            for _ in range(mult):
                numer, n = np.polydiv(numer, monomial)
                r = n[0] / d[0]
                numer = np.polysub(numer, r * factor)
                block.append(r)

            residues.extend(reversed(block))

    return np.asarray(residues)

