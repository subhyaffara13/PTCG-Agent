
def test_issue_15583():

    N = mechanics.ReferenceFrame('N')
    result = '(n_x, n_y, n_z)'
    e = pretty((N.x, N.y, N.z))
    assert e == result

