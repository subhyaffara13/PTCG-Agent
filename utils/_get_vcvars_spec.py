
def _get_vcvars_spec(host_platform, platform):
    """
    Given a host platform and platform, determine the spec for vcvarsall.

    Uses the native MSVC host if the host platform would need expensive
    emulation for x86.

    >>> _get_vcvars_spec('win-arm64', 'win32')
    'arm64_x86'
    >>> _get_vcvars_spec('win-arm64', 'win-amd64')
    'arm64_amd64'

    Otherwise, always cross-compile from x86 to work with the
    lighter-weight MSVC installs that do not include native 64-bit tools.

    >>> _get_vcvars_spec('win32', 'win32')
    'x86'
    >>> _get_vcvars_spec('win-arm32', 'win-arm32')
    'x86_arm'
    >>> _get_vcvars_spec('win-amd64', 'win-arm64')
    'x86_arm64'
    """
    if host_platform != 'win-arm64':
        host_platform = 'win32'
    vc_hp = _vcvars_names[host_platform]
    vc_plat = _vcvars_names[platform]
    return vc_hp if vc_hp == vc_plat else f'{vc_hp}_{vc_plat}'

