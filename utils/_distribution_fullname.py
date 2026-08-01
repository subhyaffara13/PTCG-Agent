
def _distribution_fullname(name: str, version: str) -> str:
    """
    >>> _distribution_fullname('setup.tools', '1.0-2')
    'setup_tools-1.0.post2'
    >>> _distribution_fullname('setup-tools', '1.2post2')
    'setup_tools-1.2.post2'
    >>> _distribution_fullname('setup-tools', '1.0-r2')
    'setup_tools-1.0.post2'
    >>> _distribution_fullname('setup.tools', '1.0.post')
    'setup_tools-1.0.post0'
    >>> _distribution_fullname('setup.tools', '1.0+ubuntu-1')
    'setup_tools-1.0+ubuntu.1'
    """
    return "{}-{}".format(
        canonicalize_name(name).replace('-', '_'),
        canonicalize_version(version, strip_trailing_zero=False),
    )

