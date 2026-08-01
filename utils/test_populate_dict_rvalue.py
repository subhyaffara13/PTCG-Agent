
def test_populate_dict_rvalue():
    pop = 1000
    my_dict = {i: i for i in range(pop)}
    assert m.populate_dict_rvalue(pop) == my_dict

