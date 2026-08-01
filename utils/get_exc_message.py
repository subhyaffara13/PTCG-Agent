
def get_exc_message(
    e: Exception, compile_id: CompileId
) -> tuple[str | None, int | None]:
    filename = None
    lineno = None
    if e.innermost_user_frame_summary is not None:  # type: ignore[attr-defined]
        filename = e.innermost_user_frame_summary.filename  # type: ignore[attr-defined]
        lineno = e.innermost_user_frame_summary.lineno  # type: ignore[attr-defined]
    e.compile_id = compile_id  # type: ignore[attr-defined]
    return filename, lineno

