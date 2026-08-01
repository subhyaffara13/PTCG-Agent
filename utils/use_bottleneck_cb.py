
def use_bottleneck_cb(key: str) -> None:
    from pandas.core import nanops

    nanops.set_use_bottleneck(cf.get_option(key))

