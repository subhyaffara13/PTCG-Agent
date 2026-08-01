
def kmp_table(word):
    """Build the 'partial match' table of the Knuth-Morris-Pratt algorithm.

    Note: This is applicable to strings or
    quantum circuits represented as tuples.
    """

    # Current position in subcircuit
    pos = 2
    # Beginning position of candidate substring that
    # may reappear later in word
    cnd = 0
    # The 'partial match' table that helps one determine
    # the next location to start substring search
    table = []
    table.append(-1)
    table.append(0)

    while pos < len(word):
        if word[pos - 1] == word[cnd]:
            cnd = cnd + 1
            table.append(cnd)
            pos = pos + 1
        elif cnd > 0:
            cnd = table[cnd]
        else:
            table.append(0)
            pos = pos + 1

    return table

