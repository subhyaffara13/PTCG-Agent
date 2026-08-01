
def _rem_redundancy(l1, terms):
    """
    After the truth table has been sufficiently simplified, use the prime
    implicant table method to recognize and eliminate redundant pairs,
    and return the essential arguments.
    """

    if not terms:
        return []

    nterms = len(terms)
    nl1 = len(l1)

    # Create dominating matrix
    dommatrix = [[0]*nl1 for n in range(nterms)]
    colcount = [0]*nl1
    rowcount = [0]*nterms
    for primei, prime in enumerate(l1):
        for termi, term in enumerate(terms):
            # Check prime implicant covering term
            if all(t == 3 or t == mt for t, mt in zip(prime, term)):
                dommatrix[termi][primei] = 1
                colcount[primei] += 1
                rowcount[termi] += 1

    # Keep track if anything changed
    anythingchanged = True
    # Then, go again
    while anythingchanged:
        anythingchanged = False

        for rowi in range(nterms):
            # Still non-dominated?
            if rowcount[rowi]:
                row = dommatrix[rowi]
                for row2i in range(nterms):
                    # Still non-dominated?
                    if rowi != row2i and rowcount[rowi] and (rowcount[rowi] <= rowcount[row2i]):
                        row2 = dommatrix[row2i]
                        if all(row2[n] >= row[n] for n in range(nl1)):
                            # row2 dominating row, remove row2
                            rowcount[row2i] = 0
                            anythingchanged = True
                            for primei, prime in enumerate(row2):
                                if prime:
                                    # Make corresponding entry 0
                                    dommatrix[row2i][primei] = 0
                                    colcount[primei] -= 1

        colcache = {}

        for coli in range(nl1):
            # Still non-dominated?
            if colcount[coli]:
                if coli in colcache:
                    col = colcache[coli]
                else:
                    col = [dommatrix[i][coli] for i in range(nterms)]
                    colcache[coli] = col
                for col2i in range(nl1):
                    # Still non-dominated?
                    if coli != col2i and colcount[col2i] and (colcount[coli] >= colcount[col2i]):
                        if col2i in colcache:
                            col2 = colcache[col2i]
                        else:
                            col2 = [dommatrix[i][col2i] for i in range(nterms)]
                            colcache[col2i] = col2
                        if all(col[n] >= col2[n] for n in range(nterms)):
                            # col dominating col2, remove col2
                            colcount[col2i] = 0
                            anythingchanged = True
                            for termi, term in enumerate(col2):
                                if term and dommatrix[termi][col2i]:
                                    # Make corresponding entry 0
                                    dommatrix[termi][col2i] = 0
                                    rowcount[termi] -= 1

        if not anythingchanged:
            # Heuristically select the prime implicant covering most terms
            maxterms = 0
            bestcolidx = -1
            for coli in range(nl1):
                s = colcount[coli]
                if s > maxterms:
                    bestcolidx = coli
                    maxterms = s

            # In case we found a prime implicant covering at least two terms
            if bestcolidx != -1 and maxterms > 1:
                for primei, prime in enumerate(l1):
                    if primei != bestcolidx:
                        for termi, term in enumerate(colcache[bestcolidx]):
                            if term and dommatrix[termi][primei]:
                                # Make corresponding entry 0
                                dommatrix[termi][primei] = 0
                                anythingchanged = True
                                rowcount[termi] -= 1
                                colcount[primei] -= 1

    return [l1[i] for i in range(nl1) if colcount[i]]

