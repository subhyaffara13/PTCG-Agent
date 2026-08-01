
def action_by_type(obj):
    '''Determine an action and a type for the given object if possible.'''
    kw = {}
    if isinstance(obj, bool):
        return {'action': ['store_true', 'store_false'][obj]}
    elif isinstance(obj, list):
        kw = {'action': 'append'}
    kw.update(get_type(obj))
    return kw

