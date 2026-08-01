
def test_block_dispatcher():
    class ArrayLike:
        pass
    a = ArrayLike()
    b = ArrayLike()
    c = ArrayLike()
    assert_equal(list(_block_dispatcher(a)), [a])
    assert_equal(list(_block_dispatcher([a])), [a])
    assert_equal(list(_block_dispatcher([a, b])), [a, b])
    assert_equal(list(_block_dispatcher([[a], [b, [c]]])), [a, b, c])
    # don't recurse into non-lists
    assert_equal(list(_block_dispatcher((a, b))), [(a, b)])

