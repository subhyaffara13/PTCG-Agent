
def _Lookup_PairPos_subtables_canonicalize(lst, font):
    """Merge multiple Format1 subtables at the beginning of lst,
    and merge multiple consecutive Format2 subtables that have the same
    Class2 (ie. were split because of offset overflows).  Returns new list."""
    lst = list(lst)

    l = len(lst)
    i = 0
    while i < l and lst[i].Format == 1:
        i += 1
    lst[:i] = [_Lookup_PairPosFormat1_subtables_flatten(lst[:i], font)]

    l = len(lst)
    i = l
    while i > 0 and lst[i - 1].Format == 2:
        i -= 1
    lst[i:] = [_Lookup_PairPosFormat2_subtables_flatten(lst[i:], font)]

    return lst

