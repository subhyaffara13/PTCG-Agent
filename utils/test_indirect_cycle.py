
def test_indirect_cycle(gc_tester):
    obj = m.OwnsPythonObjects()
    obj_list = [obj]
    obj.value = obj_list
    gc_tester(obj)

