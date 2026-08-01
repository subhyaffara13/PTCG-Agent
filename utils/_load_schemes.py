
def _load_schemes():
    """
    Extend default schemes with schemes from sysconfig.
    """

    sysconfig_schemes = _load_sysconfig_schemes() or {}

    return {
        scheme: {
            **INSTALL_SCHEMES.get(scheme, {}),
            **sysconfig_schemes.get(scheme, {}),
        }
        for scheme in set(itertools.chain(INSTALL_SCHEMES, sysconfig_schemes))
    }

