
def slowTestIf(condition):
    return slowTest if condition else lambda fn: fn

