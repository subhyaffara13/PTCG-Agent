
def test__partition_rec():
    A000041 = [1, 1, 2, 3, 5, 7, 11, 15, 22, 30, 42, 56, 77, 101, 135,
               176, 231, 297, 385, 490, 627, 792, 1002, 1255, 1575]
    for n, val in enumerate(A000041):
        assert _partition_rec(n) == val

