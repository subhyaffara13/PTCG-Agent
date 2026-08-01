
def filter_out(strings, patterns):
    '''Filter out any string that matches any of the specified patterns.'''
    for s in strings:
        if all(not fnmatch.fnmatch(s, p) for p in patterns):
            yield s

