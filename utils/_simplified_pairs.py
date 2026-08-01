
def _simplified_pairs(terms):
    """
    Reduces a set of minterms, if possible, to a simplified set of minterms
    with one less variable in the terms using QM method.
    """
    if not terms:
        return []

    simplified_terms = []
    todo = list(range(len(terms)))

    # Count number of ones as _check_pair can only potentially match if there
    # is at most a difference of a single one
    termdict = defaultdict(list)
    for n, term in enumerate(terms):
        ones = sum(1 for t in term if t == 1)
        termdict[ones].append(n)

    variables = len(terms[0])
    for k in range(variables):
        for i in termdict[k]:
            for j in termdict[k+1]:
                index = _check_pair(terms[i], terms[j])
                if index != -1:
                    # Mark terms handled
                    todo[i] = todo[j] = None
                    # Copy old term
                    newterm = terms[i][:]
                    # Set differing position to don't care
                    newterm[index] = 3
                    # Add if not already there
                    if newterm not in simplified_terms:
                        simplified_terms.append(newterm)

    if simplified_terms:
        # Further simplifications only among the new terms
        simplified_terms = _simplified_pairs(simplified_terms)

    # Add remaining, non-simplified, terms
    simplified_terms.extend([terms[i] for i in todo if i is not None])
    return simplified_terms

