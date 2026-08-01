
def _intypes(object):
    '''check if object is in the 'types' module'''
    import types
    # allow user to pass in object or object.__name__
    if type(object) is not type(''):
        object = getname(object, force=True)
    if object == 'ellipsis': object = 'EllipsisType'
    return True if hasattr(types, object) else False

