
def rotate_l(L, k):
    '''
    Rotates left by k. L is a row of a matrix or a list.

    '''
    ll = list(L)
    if ll == []:
        return []
    for i in range(k):
        el = ll.pop(0)
        ll.insert(len(ll) - 1, el)
    return ll if isinstance(L, list) else Matrix([ll])

