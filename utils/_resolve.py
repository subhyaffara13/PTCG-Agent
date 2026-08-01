
def _resolve(env: None) -> os._Environ[str]: ...


def _resolve(env: _MappingT) -> _MappingT: ...


def _resolve(env: _MappingT | None) -> _MappingT | os._Environ[str]:
    return os.environ if env is None else env

