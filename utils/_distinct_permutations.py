
def _distinct_permutations(iterable):
    """
    Find the number of distinct permutations of elements of `iterable`.
    """

    # Algorithm: https://w.wiki/Qai

    items = sorted(iterable)
    size = len(items)

    while True:
        # Yield the permutation we have
        yield tuple(items)

        # Find the largest index i such that A[i] < A[i + 1]
        for i in range(size - 2, -1, -1):
            if items[i] < items[i + 1]:
                break

        #  If no such index exists, this permutation is the last one
        else:
            return

        # Find the largest index j greater than j such that A[i] < A[j]
        for j in range(size - 1, i, -1):
            if items[i] < items[j]:
                break

        # Swap the value of A[i] with that of A[j], then reverse the
        # sequence from A[i + 1] to form the new permutation
        items[i], items[j] = items[j], items[i]
        items[i+1:] = items[:i-size:-1]  # A[i + 1:][::-1]

