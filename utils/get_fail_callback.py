from typing import Any

def get_fail_callback(callback: ConvertFrameProtocol) -> ConvertFrameProtocol:
    fail_callback = getattr(callback, "_dynamo_fail_callback", None)
    if fail_callback is not None:
        return fail_callback

    def compile_frame_error(*args: Any, **kwargs: Any) -> NoReturn:
        raise RuntimeError(
            "Dynamo: expected not to compile nested code - this happens because "
            "a Dynamo callback was triggered and succeeded in compiling "
            "when running fullgraph=True compiled code."
        )

    def fail_callback(*args: Any, **kwargs: Any) -> ConvertFrameReturn:
        with mock.patch(__name__ + ".compile_frame", compile_frame_error):
            return callback(*args, **kwargs)

    # pyrefly: ignore [missing-attribute]
    callback._dynamo_fail_callback = fail_callback
    return fail_callback

