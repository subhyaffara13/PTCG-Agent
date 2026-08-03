import os

def test_tempdir():
    with tempdir() as tdir:
        fpath = os.path.join(tdir, 'tmp')
        with open(fpath, 'w'):
            pass
    assert_(not os.path.isdir(tdir))

    raised = False
    try:
        with tempdir() as tdir:
            raise ValueError
    except ValueError:
        raised = True
    assert_(raised)
    assert_(not os.path.isdir(tdir))

