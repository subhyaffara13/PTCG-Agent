
def test_eigenvects():
    M = Matrix([[0, 1, 1],
                [1, 0, 0],
                [1, 1, 1]])
    vecs = M.eigenvects()
    for val, mult, vec_list in vecs:
        assert len(vec_list) == 1
        assert M*vec_list[0] == val*vec_list[0]

