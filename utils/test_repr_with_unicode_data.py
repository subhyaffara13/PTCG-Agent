
def test_repr_with_unicode_data():
    with pd.option_context("display.encoding", "UTF-8"):
        d = {"a": ["\u05d0", 2, 3], "b": [4, 5, 6], "c": [7, 8, 9]}
        index = pd.DataFrame(d).set_index(["a", "b"]).index
        assert "\\" not in repr(index)  # we don't want unicode-escaped

