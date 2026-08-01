
def test_shared_ptr_gc():
    """#187: issue involving std::shared_ptr<> return value policy & garbage collection"""
    el = m.ElementList()
    for i in range(10):
        el.add(m.ElementA(i))
    pytest.gc_collect()
    for i, v in enumerate(el.get()):
        assert i == v.value()

