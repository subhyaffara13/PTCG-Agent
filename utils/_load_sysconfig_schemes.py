
def _load_sysconfig_schemes():
    with contextlib.suppress(AttributeError):
        return {
            scheme: sysconfig.get_paths(scheme, expand=False)
            for scheme in sysconfig.get_scheme_names()
        }

