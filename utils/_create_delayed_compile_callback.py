from typing import Any, Callable

def _create_delayed_compile_callback(
    callback: DynamoCallback, stance: str
) -> Callable[..., Any]:
    def callback_fn(*args: Any, **kwargs: Any) -> convert_frame.ConvertFrameReturn:
        frame = args[0]
        example_inputs = _get_or_add_example_inputs(frame)

        if len(example_inputs) == 1:
            if stance == "eager_then_compile":
                return ConvertFrameReturn(
                    frame_exec_strategy=FrameExecStrategy(
                        FrameAction.DEFAULT, FrameAction.DEFAULT
                    )
                )
            elif stance == "aot_eager_then_compile":
                aot_eager_fn = get_compiler_fn("aot_eager")
                return _create_wrapped_callback(aot_eager_fn)(*args, **kwargs)

        dynamism = track_dynamism_across_examples(example_inputs)
        code_context.get_context(frame.f_code)["dynamism"] = dynamism
        compiler_fn = callback._torchdynamo_orig_backend._torchdynamo_orig_backend  # type: ignore[union-attr]
        return _create_wrapped_callback(compiler_fn)(*args, **kwargs)

    # to prevent cache miss due to different backend
    callback_fn._torchdynamo_orig_backend = callback  # type: ignore[attr-defined]

    return callback_fn

