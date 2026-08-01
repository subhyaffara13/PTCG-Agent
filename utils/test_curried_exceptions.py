
def test_curried_exceptions():
    # This tests a global curried object that isn't defined in toolz.functoolz
    merge = pickle.loads(pickle.dumps(toolz.curried.merge))
    assert merge is toolz.curried.merge

