
def register_converter_cb(key: str) -> None:
    from pandas.plotting import (
        deregister_matplotlib_converters,
        register_matplotlib_converters,
    )

    if cf.get_option(key):
        register_matplotlib_converters()
    else:
        deregister_matplotlib_converters()

