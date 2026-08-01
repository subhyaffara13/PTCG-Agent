
def test_integer_hash_collision_dict():
    # GH 30013
    result = {NA: "foo", hash(NA): "bar"}

    assert result[NA] == "foo"
    assert result[hash(NA)] == "bar"

