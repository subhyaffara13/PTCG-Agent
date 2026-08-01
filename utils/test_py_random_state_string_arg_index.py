
def test_py_random_state_string_arg_index():
    with pytest.raises(nx.NetworkXError):

        @py_random_state("a")
        def make_random_state(rs):
            pass

        rstate = make_random_state(1)

