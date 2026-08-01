
def test_and():
    variables = x, y
    expected = ({x: z > 0, y: n < 3},)
    assert iterdicteq(unify((z>0) & (n<3), And(x, y), variables=variables),
                      expected)

