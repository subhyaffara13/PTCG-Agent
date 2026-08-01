
def test_hash_vs_typeinfo_2():
    """different typeinfo should mean !eq"""
    # the following two are semantically different
    x = Symbol('x')
    x1 = Symbol('x', even=True)

    assert x != x1
    assert hash(x) != hash(x1)  # This might fail with very low probability

