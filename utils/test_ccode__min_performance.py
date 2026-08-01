
def test_ccode_Min_performance():
    #Shouldn't take more than a few seconds
    big_min = Min(*symbols('a[0:50]'))
    for curr_standard in ('c89', 'c99', 'c11'):
        output = ccode(big_min, standard=curr_standard)
        assert output.count('(') == output.count(')')

