
def test_numpy_reloading():
    # gh-7844. Also check that relevant globals retain their identity.
    import numpy as np
    import numpy._globals

    _NoValue = np._NoValue
    VisibleDeprecationWarning = ex.VisibleDeprecationWarning
    ModuleDeprecationWarning = ex.ModuleDeprecationWarning

    with pytest.warns(UserWarning):
        reload(np)
    assert_(_NoValue is np._NoValue)
    assert_(ModuleDeprecationWarning is ex.ModuleDeprecationWarning)
    assert_(VisibleDeprecationWarning is ex.VisibleDeprecationWarning)

    assert_raises(RuntimeError, reload, numpy._globals)
    with pytest.warns(UserWarning):
        reload(np)
    assert_(_NoValue is np._NoValue)
    assert_(ModuleDeprecationWarning is ex.ModuleDeprecationWarning)
    assert_(VisibleDeprecationWarning is ex.VisibleDeprecationWarning)

