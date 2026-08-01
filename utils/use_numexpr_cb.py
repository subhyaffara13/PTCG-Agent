
def use_numexpr_cb(key: str) -> None:
    from pandas.core.computation import expressions

    expressions.set_use_numexpr(cf.get_option(key))

