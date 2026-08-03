import copy

def test_property_return_value_policies(access):
    obj = m.TestPropRVP() if not access.startswith("static") else m.TestPropRVP

    ref = getattr(obj, access + "_ref")
    assert ref.value == 1
    ref.value = 2
    assert getattr(obj, access + "_ref").value == 2
    ref.value = 1  # restore original value for static properties

    copy = getattr(obj, access + "_copy")
    assert copy.value == 1
    copy.value = 2
    assert getattr(obj, access + "_copy").value == 1

    copy = getattr(obj, access + "_func")
    assert copy.value == 1
    copy.value = 2
    assert getattr(obj, access + "_func").value == 1

