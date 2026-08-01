
def getopt(name):
    '''
        :param name: Name of option to return.
    '''
    # also allows for: Script.foo
    return getattr(program, name)

