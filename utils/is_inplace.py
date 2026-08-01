
def is_inplace(func):
    name = func.overloadpacket.__name__
    if re.match('__i.+__', name):
        return True
    if re.match('__.+__', name):
        return False
    return name[-1] == '_'

