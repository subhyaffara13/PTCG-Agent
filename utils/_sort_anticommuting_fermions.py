
def _sort_anticommuting_fermions(string1, key=_sqkey_operator):
    """Sort fermionic operators to canonical order, assuming all pairs anticommute.

    Explanation
    ===========

    Uses a bidirectional bubble sort.  Items in string1 are not referenced
    so in principle they may be any comparable objects.   The sorting depends on the
    operators '>' and '=='.

    If the Pauli principle is violated, an exception is raised.

    Returns
    =======

    tuple (sorted_str, sign)

    sorted_str: list containing the sorted operators
    sign: int telling how many times the sign should be changed
          (if sign==0 the string was already sorted)
    """

    verified = False
    sign = 0
    rng = list(range(len(string1) - 1))
    rev = list(range(len(string1) - 3, -1, -1))

    keys = list(map(key, string1))
    key_val = dict(list(zip(keys, string1)))

    while not verified:
        verified = True
        for i in rng:
            left = keys[i]
            right = keys[i + 1]
            if left == right:
                raise ViolationOfPauliPrinciple([left, right])
            if left > right:
                verified = False
                keys[i:i + 2] = [right, left]
                sign = sign + 1
        if verified:
            break
        for i in rev:
            left = keys[i]
            right = keys[i + 1]
            if left == right:
                raise ViolationOfPauliPrinciple([left, right])
            if left > right:
                verified = False
                keys[i:i + 2] = [right, left]
                sign = sign + 1
    string1 = [ key_val[k] for k in keys ]
    return (string1, sign)

