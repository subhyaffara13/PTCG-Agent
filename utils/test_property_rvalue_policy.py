
def test_property_rvalue_policy():
    """When returning an rvalue, the return value policy is automatically changed from
    `reference(_internal)` to `move`. The following would not work otherwise."""

    instance = m.TestPropRVP()
    o = instance.rvalue
    assert o.value == 1

    os = m.TestPropRVP.static_rvalue
    assert os.value == 1

