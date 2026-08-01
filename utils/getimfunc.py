
def getimfunc(func):
    try:
        return func.__func__
    except AttributeError:
        return func

