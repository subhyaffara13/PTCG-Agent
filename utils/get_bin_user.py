
def get_bin_user() -> str:
    return _sysconfig.get_scheme("", user=True).scripts

