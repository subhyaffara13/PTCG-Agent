
def xfailIf(condition):
    def wrapper(func):
        if condition:
            return unittest.expectedFailure(func)
        else:
            return func
    return wrapper

