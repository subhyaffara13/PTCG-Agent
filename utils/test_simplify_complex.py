
def test_simplify_complex():
    cosAsExp = cos(x)._eval_rewrite_as_exp(x)
    tanAsExp = tan(x)._eval_rewrite_as_exp(x)
    assert simplify(cosAsExp*tanAsExp) == sin(x) # issue 4341

    # issue 10124
    assert simplify(exp(Matrix([[0, -1], [1, 0]]))) == Matrix([[cos(1),
        -sin(1)], [sin(1), cos(1)]])

