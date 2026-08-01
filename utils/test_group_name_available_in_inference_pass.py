
def test_group_name_available_in_inference_pass():
    # gh-15062
    df = DataFrame({"a": [0, 0, 1, 1, 2, 2], "b": np.arange(6)})

    names = []

    def f(group):
        names.append(group.name)
        return group.copy()

    df.groupby("a", sort=False, group_keys=False).apply(f)
    expected_names = [0, 1, 2]
    assert names == expected_names

