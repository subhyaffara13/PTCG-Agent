
def _isstring(object): #XXX: isstringlike better?
    '''check if object is a string-like type'''
    return isinstance(object, (str, bytes))


def _isstring(var):
    return 'typespec' in var and var['typespec'] == 'character' and \
           not isexternal(var)

