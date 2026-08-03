import re

def test_merge_datetime_and_timedelta(how):
    left = DataFrame({"key": Series([1, None], dtype="datetime64[ns]")})
    right = DataFrame({"key": Series([1], dtype="timedelta64[ns]")})

    msg = (
        f"You are trying to merge on {left['key'].dtype} and {right['key'].dtype} "
        "columns for key 'key'. If you wish to proceed you should use pd.concat"
    )
    with pytest.raises(ValueError, match=re.escape(msg)):
        left.merge(right, on="key", how=how)

    msg = (
        f"You are trying to merge on {right['key'].dtype} and {left['key'].dtype} "
        "columns for key 'key'. If you wish to proceed you should use pd.concat"
    )
    with pytest.raises(ValueError, match=re.escape(msg)):
        right.merge(left, on="key", how=how)

