
def test_insert_base(idx):
    result = idx[1:4]

    # test 0th element
    assert idx[0:4].equals(result.insert(0, idx[0]))

