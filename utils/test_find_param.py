
def test_find_param(doc, params):
        found_params = find_param_docs(doc)
        assert params.keys() == found_params.keys()
        for key, value in params.items():
            assert key in found_params
            found_value = found_params[key]
            assert value[0] == found_value[0]
            for kwarg, val in value[1].items():
                assert val == found_value[1][kwarg]

