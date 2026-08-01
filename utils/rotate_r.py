
def rotate_r(L, k):
    '''
    Rotates right by k. L is a row of a matrix or a list.

    '''
    ll = list(L)
    if ll == []:
        return []
    for i in range(k):
        el = ll.pop(len(ll) - 1)
        ll.insert(0, el)
    return ll if isinstance(L, list) else Matrix([ll])

