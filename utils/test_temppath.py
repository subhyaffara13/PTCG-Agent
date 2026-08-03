import os

def test_temppath():
    with temppath() as fpath:
        with open(fpath, 'w'):
            pass
    assert_(not os.path.isfile(fpath))

    raised = False
    try:
        with temppath() as fpath:
            raise ValueError
    except ValueError:
        raised = True
    assert_(raised)
    assert_(not os.path.isfile(fpath))

