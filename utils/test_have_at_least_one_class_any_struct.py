
def test_have_at_least_one_class_any_struct():
    assert (
        m.unnamed_namespace_a_any_struct is not None
        or mb.unnamed_namespace_b_any_struct is not None
    )

