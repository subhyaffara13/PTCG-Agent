
def test_DomainMatrix_to_flat_nz():
    Adm = DM([[1, 2], [3, 0]], ZZ)
    Addm = Adm.rep.to_ddm()
    Asdm = Adm.rep.to_sdm()
    for A in [Adm, Addm, Asdm]:
        elems, data = A.to_flat_nz()
        assert A.from_flat_nz(elems, data, A.domain) == A
        elemsq = [QQ(e) for e in elems]
        assert A.from_flat_nz(elemsq, data, QQ) == A.convert_to(QQ)
        elems2 = [2*e for e in elems]
        assert A.from_flat_nz(elems2, data, A.domain) == 2*A

