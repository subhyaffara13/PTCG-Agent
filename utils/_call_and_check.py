
def _call_and_check(
    klass, msg, how, gb, groupby_func, args, warn_category=None, warn_msg=""
):
    with tm.assert_produces_warning(
        warn_category, match=warn_msg, check_stacklevel=False
    ):
        if klass is None:
            if how == "method":
                getattr(gb, groupby_func)(*args)
            elif how == "agg":
                gb.agg(groupby_func, *args)
            else:
                gb.transform(groupby_func, *args)
        else:
            with pytest.raises(klass, match=msg):
                if how == "method":
                    getattr(gb, groupby_func)(*args)
                elif how == "agg":
                    gb.agg(groupby_func, *args)
                else:
                    gb.transform(groupby_func, *args)

