from typing import Any, Callable

def deserialize_bundled_cache_entry(
    entry: BundledAOTAutogradResult[Any],
) -> Callable[..., Any]:
    from copy import deepcopy

    from torch._inductor.cudagraph_utils import BoxedDeviceIndex
    from torch._inductor.utils import BoxedBool

    # In the precompile use case, guards are already serialized
    # by dynamo, so we don't need to add them to the environment
    entry.guards_expr = None
    # TODO: this isn't exactly right, because cudagraphs needs to be a shared config
    # which is set by compile_fx. But in precompile, we never actually call compile_fx
    # so we don't have a place to track cudagraphs here.
    cudagraphs = BoxedBool(torch._inductor.config.triton.cudagraphs)
    boxed_forward_device_index = BoxedDeviceIndex(None)
    # We need to make a clean copy of the cache entry
    # in case it needs to be serialized again
    serializable_copy = deepcopy(entry)

    from torch._subclasses import FakeTensorMode
    from torch.fx.experimental.symbolic_shapes import ShapeEnv

    context = torch._guards.TracingContext.try_get()
    if context is None:
        # Create a clean environment when running fx graph post compile
        # if one is not available
        context = torch._guards.TracingContext(FakeTensorMode(shape_env=ShapeEnv()))
    with torch._guards.tracing(context):
        compiled_fn = entry.wrap_post_compile(
            [],
            entry.sanitized_aot_config,
            {
                "cudagraphs": cudagraphs,
                "boxed_forward_device_index": boxed_forward_device_index,
            },
        )
    # Ensure the deserialized cache entry is still serializable

    compiled_fn = SerializableCompiledFunction(compiled_fn, lambda: serializable_copy)

    # TODO: this ignores flat_params, which can exist
    # if inline_builtin_nn_modules=False
    @simple_wraps(compiled_fn)
    def forward(*runtime_args: Any) -> Any:
        return compiled_fn(list(runtime_args))

    if not hasattr(compiled_fn, "serialize"):
        raise AssertionError("compiled_fn must have serialize attribute")
    forward.serialize = compiled_fn.serialize  # type: ignore[attr-defined]

    return forward

