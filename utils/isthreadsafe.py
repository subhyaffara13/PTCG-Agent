
def isthreadsafe(rout):
    return 'f2pyenhancements' in rout and \
           'threadsafe' in rout['f2pyenhancements']

