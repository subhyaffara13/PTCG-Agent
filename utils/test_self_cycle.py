
def test_self_cycle(gc_tester):
    obj = m.OwnsPythonObjects()
    obj.value = obj
    gc_tester(obj)

