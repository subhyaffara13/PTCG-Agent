
def isdynamic(obj):
    "check if object was built in the interpreter"
    try: file = getfile(obj)
    except TypeError: file = None
    if file == '<stdin>' and isfrommain(obj):
        return True
    return False

