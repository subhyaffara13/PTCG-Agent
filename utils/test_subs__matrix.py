
def test_subs_Matrix():
    z = zeros(2)
    z1 = ZeroMatrix(2, 2)
    assert (x*y).subs({x:z, y:0}) in [z, z1]
    assert (x*y).subs({y:z, x:0}) == 0
    assert (x*y).subs({y:z, x:0}, simultaneous=True) in [z, z1]
    assert (x + y).subs({x: z, y: z}, simultaneous=True) in [z, z1]
    assert (x + y).subs({x: z, y: z}) in [z, z1]

    # Issue #15528
    assert Mul(Matrix([[3]]), x).subs(x, 2.0) == Matrix([[6.0]])
    # Does not raise a TypeError, see comment on the MatAdd postprocessor
    assert Add(Matrix([[3]]), x).subs(x, 2.0) == Add(Matrix([[3]]), 2.0)

