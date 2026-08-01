
def test_transform_passes_args(use_apply, frame_or_series):
    # GH 35964
    # transform uses UDF either via apply or passing the entire DataFrame
    expected_args = [1, 2]
    expected_kwargs = {"c": 3}

    def f(x, a, b, c):
        # transform is using apply iff x is not a DataFrame
        if use_apply == isinstance(x, frame_or_series):
            # Force transform to fallback
            raise ValueError
        assert [a, b] == expected_args
        assert c == expected_kwargs["c"]
        return x

    frame_or_series([1]).transform(f, 0, *expected_args, **expected_kwargs)

