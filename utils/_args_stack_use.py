
def _argsStackUse(args):
    stackLen = 0
    maxLen = 0
    for arg in args:
        if type(arg) is list:
            # Blended arg
            maxLen = max(maxLen, stackLen + _argsStackUse(arg))
            stackLen += arg[-1]
        else:
            stackLen += 1
    return max(stackLen, maxLen)

