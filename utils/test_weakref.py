
def test_weakref(create_weakref, create_weakref_with_callback):
    from weakref import getweakrefcount

    # Apparently, you cannot weakly reference an object()
    class WeaklyReferenced:
        pass

    callback_called = False

    def callback(_):
        nonlocal callback_called
        callback_called = True

    obj = WeaklyReferenced()
    assert getweakrefcount(obj) == 0
    wr = create_weakref(obj)
    assert getweakrefcount(obj) == 1

    obj = WeaklyReferenced()
    assert getweakrefcount(obj) == 0
    wr = create_weakref_with_callback(obj, callback)  # noqa: F841
    assert getweakrefcount(obj) == 1
    assert not callback_called
    del obj
    pytest.gc_collect()
    assert callback_called


def test_weakref():
    o = _class()
    oc = _callable_class()
    f = _function
    x = _class

    # ReferenceType
    r = weakref.ref(o)
    d_r = weakref.ref(_class())
    fr = weakref.ref(f)
    xr = weakref.ref(x)

    # ProxyType
    p = weakref.proxy(o)
    d_p = weakref.proxy(_class())

    # CallableProxyType
    cp = weakref.proxy(oc)
    d_cp = weakref.proxy(_callable_class())
    fp = weakref.proxy(f)
    xp = weakref.proxy(x)

    objlist = [r,d_r,fr,xr, p,d_p, cp,d_cp,fp,xp]
    #dill.detect.trace(True)

    for obj in objlist:
      res = dill.detect.errors(obj)
      if res:
        print ("%r:\n  %s" % (obj, res))
    # else:
    #   print ("PASS: %s" % obj)
      assert not res

