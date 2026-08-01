
def test_class_refcount():
    """Instances must correctly increase/decrease the reference count of their types (#1029)"""
    from sys import getrefcount

    class PyDog(m.Dog):
        pass

    for cls in m.Dog, PyDog:
        refcount_1 = getrefcount(cls)
        molly = [cls("Molly") for _ in range(10)]
        refcount_2 = getrefcount(cls)

        del molly
        pytest.gc_collect()
        refcount_3 = getrefcount(cls)

        assert refcount_1 == refcount_3
        assert refcount_2 > refcount_1

