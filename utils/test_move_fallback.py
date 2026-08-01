
def test_move_fallback():
    """#389: rvp::move should fall-through to copy on non-movable objects"""

    m1 = m.get_moveissue1(1)
    assert m1.value == 1
    m2 = m.get_moveissue2(2)
    assert m2.value == 2

