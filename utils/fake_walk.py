
def fake_walk(start):
    dirs = ['tests', 'sub', '.hid']
    contents = {
        'tests': ['test_amod.py', 'run.py', '.hid.py'],
        'sub': ['amod.py', 'bmod.py'],
    }
    yield '.', dirs, ['tox.ini', 'amod.py', 'test_all.py', 'fake.yp', 'noext']
    for d in dirs:
        yield './{0}'.format(d), [], contents[d]

