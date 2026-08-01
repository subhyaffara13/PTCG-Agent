
def test_PermutationMatrix():
    p = Permutation(0, 1, 2)
    assert latex(PermutationMatrix(p)) == r'P_{\left( 0\; 1\; 2\right)}'
    p = Permutation(0, 3)(1, 2)
    assert latex(PermutationMatrix(p)) == \
        r'P_{\left( 0\; 3\right)\left( 1\; 2\right)}'

