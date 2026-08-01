
def test_ccode_Max():
    # Test for gh-11926
    assert ccode(Max(x,x*x),user_functions={"Max":"my_max", "Pow":"my_pow"}) == 'my_max(x, my_pow(x, 2))'

