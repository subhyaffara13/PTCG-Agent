
def get_compile_id(
    frame_state: dict[str, int | FrameStateSizeEntry],
) -> CompileId:
    global FRAME_COUNTER
    if "_id" not in frame_state:
        frame_state["_id"] = FRAME_COUNTER
        FRAME_COUNTER += 1
    frame_id = frame_state["_id"]
    assert isinstance(frame_id, int)

    frame_compile_id = FRAME_COMPILE_COUNTER[frame_id]
    FRAME_COMPILE_COUNTER[frame_id] += 1

    compiled_autograd_id = None
    if prior := CompileContext.current_compile_id():
        compiled_autograd_id = prior.compiled_autograd_id
    return CompileId(
        compiled_autograd_id=compiled_autograd_id,
        frame_id=frame_id,
        frame_compile_id=frame_compile_id,
    )

