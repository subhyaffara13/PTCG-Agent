
def _inverse_permutation(perm):
    # Given a permutation, returns its inverse. It's equivalent to argsort on an array
    return [i for i, j in sorted(enumerate(perm), key=operator.itemgetter(1))]

