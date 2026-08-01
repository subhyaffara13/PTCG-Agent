
def test_DomainMatrix_content_primitive():
    A = DM([[2, 4], [6, 8]], ZZ)
    A_primitive = DM([[1, 2], [3, 4]], ZZ)
    A_content = ZZ(2)
    assert A.content() == A_content
    assert A.primitive() == (A_content, A_primitive)

