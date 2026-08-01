
def mergeObjects(lst):
    lst = [item for item in lst if item is not NotImplemented]
    if not lst:
        return NotImplemented
    lst = [item for item in lst if item is not None]
    if not lst:
        return None

    clazz = lst[0].__class__
    assert all(type(item) == clazz for item in lst), lst

    logic = clazz.mergeMap
    returnTable = clazz()
    returnDict = {}

    allKeys = set.union(set(), *(vars(table).keys() for table in lst))
    for key in allKeys:
        try:
            mergeLogic = logic[key]
        except KeyError:
            try:
                mergeLogic = logic["*"]
            except KeyError:
                raise Exception(
                    "Don't know how to merge key %s of class %s" % (key, clazz.__name__)
                )
        if mergeLogic is NotImplemented:
            continue
        value = mergeLogic(getattr(table, key, NotImplemented) for table in lst)
        if value is not NotImplemented:
            returnDict[key] = value

    returnTable.__dict__ = returnDict

    return returnTable

