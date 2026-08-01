
def _raise_wrapfail(
    wrap_controller: Generator[None, object, object],
    msg: str,
) -> NoReturn:
    co = wrap_controller.gi_code  # type: ignore[attr-defined]
    raise RuntimeError(
        f"wrap_controller at {co.co_name!r} {co.co_filename}:{co.co_firstlineno} {msg}"
    )

