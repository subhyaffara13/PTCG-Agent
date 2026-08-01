
def parseBlendList(s):
    valueList = []
    for element in s:
        if isinstance(element, str):
            continue
        name, attrs, content = element
        blendList = attrs["value"].split()
        blendList = [safeEval(val) for val in blendList]
        valueList.append(blendList)
    if len(valueList) == 1:
        valueList = valueList[0]
    return valueList

