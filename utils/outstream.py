import sys

def outstream(outfile=None):
    '''Encapsulate output stream creation as a context manager'''
    if outfile:
        with open(outfile, 'w') as outstream:
            yield outstream
    else:
        yield sys.stdout

