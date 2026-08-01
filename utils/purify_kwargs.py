
def purify_kwargs(kwargs):
    '''If type or metavar are set to None, they are removed from kwargs.'''
    for key, value in kwargs.copy().items():
        if key in set(['type', 'metavar']) and value is None:
            del kwargs[key]
    return kwargs

