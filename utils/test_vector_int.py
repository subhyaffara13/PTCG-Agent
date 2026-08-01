
def test_vector_int():
    v_int = m.VectorInt([0, 0])
    assert len(v_int) == 2
    assert bool(v_int) is True

    # test construction from a generator
    v_int1 = m.VectorInt(x for x in range(5))
    assert v_int1 == m.VectorInt([0, 1, 2, 3, 4])

    v_int2 = m.VectorInt([0, 0])
    assert v_int == v_int2
    v_int2[1] = 1
    assert v_int != v_int2

    v_int2.append(2)
    v_int2.insert(0, 1)
    v_int2.insert(0, 2)
    v_int2.insert(0, 3)
    v_int2.insert(6, 3)
    assert str(v_int2) == "VectorInt[3, 2, 1, 0, 1, 2, 3]"
    with pytest.raises(IndexError):
        v_int2.insert(8, 4)

    v_int.append(99)
    v_int2[2:-2] = v_int
    assert v_int2 == m.VectorInt([3, 2, 0, 0, 99, 2, 3])
    del v_int2[1:3]
    assert v_int2 == m.VectorInt([3, 0, 99, 2, 3])
    del v_int2[0]
    assert v_int2 == m.VectorInt([0, 99, 2, 3])

    v_int2.extend(m.VectorInt([4, 5]))
    assert v_int2 == m.VectorInt([0, 99, 2, 3, 4, 5])

    v_int2.extend([6, 7])
    assert v_int2 == m.VectorInt([0, 99, 2, 3, 4, 5, 6, 7])

    # test error handling, and that the vector is unchanged
    with pytest.raises(RuntimeError):
        v_int2.extend([8, "a"])

    assert v_int2 == m.VectorInt([0, 99, 2, 3, 4, 5, 6, 7])

    # test extending from a generator
    v_int2.extend(x for x in range(5))
    assert v_int2 == m.VectorInt([0, 99, 2, 3, 4, 5, 6, 7, 0, 1, 2, 3, 4])

    # test negative indexing
    assert v_int2[-1] == 4

    # insert with negative index
    v_int2.insert(-1, 88)
    assert v_int2 == m.VectorInt([0, 99, 2, 3, 4, 5, 6, 7, 0, 1, 2, 3, 88, 4])

    # delete negative index
    del v_int2[-1]
    assert v_int2 == m.VectorInt([0, 99, 2, 3, 4, 5, 6, 7, 0, 1, 2, 3, 88])

    v_int2.clear()
    assert len(v_int2) == 0

