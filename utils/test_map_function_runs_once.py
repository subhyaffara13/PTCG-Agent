
def test_map_function_runs_once():
    df = DataFrame({"a": [1, 2, 3]})
    values = []  # Save values function is applied to

    def reducing_function(val):
        values.append(val)

    def non_reducing_function(val):
        values.append(val)
        return val

    for func in [reducing_function, non_reducing_function]:
        del values[:]

        df.map(func)
        assert values == df.a.to_list()

