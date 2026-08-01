
def unique_key(adict):
    """ Obtain a unique key given a dictionary."""
    allkeys = list(adict.keys())
    done = False
    n = 1
    while not done:
        newkey = f'__l{n}'
        if newkey in allkeys:
            n += 1
        else:
            done = True
    return newkey

