
def ensure_dashes(opts):
    '''Ensure that the options have the right number of dashes.'''
    for opt in opts:
        if opt.startswith('-'):
            yield opt
        else:
            yield '-' * (1 + 1 * (len(opt) > 1)) + opt

