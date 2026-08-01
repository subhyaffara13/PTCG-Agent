
def Or(*args):
    """Defines the three valued ``Or`` behaviour for a 2-tuple of
     three valued logic values"""
    def reduce_or(cmp_intervala, cmp_intervalb):
        if cmp_intervala[0] is True or cmp_intervalb[0] is True:
            first = True
        elif cmp_intervala[0] is None or cmp_intervalb[0] is None:
            first = None
        else:
            first = False

        if cmp_intervala[1] is True or cmp_intervalb[1] is True:
            second = True
        elif cmp_intervala[1] is None or cmp_intervalb[1] is None:
            second = None
        else:
            second = False
        return (first, second)
    return reduce(reduce_or, args)

