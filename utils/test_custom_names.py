
def test_custom_names():
    A = CoordSys3D('A', vector_names=['x', 'y', 'z'],
                   variable_names=['i', 'j', 'k'])
    assert A.i.__str__() == 'A.i'
    assert A.x.__str__() == 'A.x'
    assert A.i._pretty_form == 'i_A'
    assert A.x._pretty_form == 'x_A'
    assert A.i._latex_form == r'\mathbf{{i}_{A}}'
    assert A.x._latex_form == r"\mathbf{\hat{x}_{A}}"

