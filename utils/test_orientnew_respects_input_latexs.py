
def test_orientnew_respects_input_latexs():
    N = ReferenceFrame('N')
    q1 = dynamicsymbols('q1')
    A = N.orientnew('a', 'Axis', [q1, N.z])

    #build default and alternate latex_vecs:
    def_latex_vecs = [(r"\mathbf{\hat{%s}_%s}" % (A.name.lower(),
                      A.indices[0])), (r"\mathbf{\hat{%s}_%s}" %
                      (A.name.lower(), A.indices[1])),
                      (r"\mathbf{\hat{%s}_%s}" % (A.name.lower(),
                      A.indices[2]))]

    name = 'b'
    indices = [x+'1' for x in N.indices]
    new_latex_vecs = [(r"\mathbf{\hat{%s}_{%s}}" % (name.lower(),
                      indices[0])), (r"\mathbf{\hat{%s}_{%s}}" %
                      (name.lower(), indices[1])),
                      (r"\mathbf{\hat{%s}_{%s}}" % (name.lower(),
                      indices[2]))]

    B = N.orientnew(name, 'Axis', [q1, N.z], latexs=new_latex_vecs)

    assert A.latex_vecs == def_latex_vecs
    assert B.latex_vecs == new_latex_vecs
    assert B.indices != indices

