
def fontInfoOpenTypeGaspRangeRecordsValidator(value: Any) -> bool:
    """
    Version 3+.
    """
    if not isinstance(value, list):
        return False
    if len(value) == 0:
        return True
    validBehaviors = [0, 1, 2, 3]
    dictPrototype: GenericDict = dict(
        rangeMaxPPEM=(int, True), rangeGaspBehavior=(list, True)
    )
    ppemOrder = []
    for rangeRecord in value:
        if not genericDictValidator(rangeRecord, dictPrototype):
            return False
        ppem = rangeRecord["rangeMaxPPEM"]
        behavior = rangeRecord["rangeGaspBehavior"]
        ppemValidity = genericNonNegativeIntValidator(ppem)
        if not ppemValidity:
            return False
        behaviorValidity = genericIntListValidator(behavior, validBehaviors)
        if not behaviorValidity:
            return False
        ppemOrder.append(ppem)
    if ppemOrder != sorted(ppemOrder):
        return False
    return True

