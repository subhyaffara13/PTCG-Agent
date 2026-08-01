
def _emscripten_platforms() -> Iterator[str]:
    pyemscripten_platform_version = sysconfig.get_config_var(
        "PYEMSCRIPTEN_PLATFORM_VERSION"
    )
    if pyemscripten_platform_version:
        yield f"pyemscripten_{pyemscripten_platform_version}_wasm32"
    yield from _generic_platforms()


def _emscripten_platforms() -> Iterator[str]:
    pyemscripten_platform_version = sysconfig.get_config_var(
        "PYEMSCRIPTEN_PLATFORM_VERSION"
    )
    if pyemscripten_platform_version:
        yield f"pyemscripten_{pyemscripten_platform_version}_wasm32"
    yield from _generic_platforms()

