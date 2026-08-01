
def _inject_macos_ver(env: _MappingT | None) -> _MappingT | dict[str, str | int] | None:
    if platform.system() != 'Darwin':
        return env

    from .util import MACOSX_VERSION_VAR, get_macosx_target_ver

    target_ver = get_macosx_target_ver()
    update = {MACOSX_VERSION_VAR: target_ver} if target_ver else {}
    return {**_resolve(env), **update}

