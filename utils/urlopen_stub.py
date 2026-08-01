
def urlopen_stub(url, data=None):
    '''Stub to replace urlopen for testing.'''
    if url == valid_httpurl():
        tmpfile = NamedTemporaryFile(prefix='urltmp_')
        return tmpfile
    else:
        raise URLError('Name or service not known')

