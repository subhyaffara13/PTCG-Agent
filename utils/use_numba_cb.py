
def use_numba_cb(key: str) -> None:
    from pandas.core.util import numba_

    numba_.set_use_numba(cf.get_option(key))

