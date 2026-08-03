from typing import Any, Callable

def _distribute_function(
    fn: Callable,
    fn_module: types.ModuleType,
    device_mesh: DeviceMesh,
    input_fn: InputFnType,
    output_fn: OutputFnType,
) -> None:
    """
    A helper function to replace a function with a distributed version by
    using the monkey patching approach.

    This function is for the CP internal usage only.
    """

    def wrapper(
        target_fn: Callable, input_fn: InputFnType, output_fn: OutputFnType
    ) -> Callable:
        def inner_fn(*args: ArgsType, **kwargs: KwargsType) -> Any:
            args, kwargs = input_fn(None, args, kwargs, device_mesh)
            outputs = target_fn(*args, **kwargs)
            return output_fn(None, (args, kwargs), outputs, device_mesh)

        return inner_fn

    global _replaced_functions

    if fn in _replaced_functions:
        return

    wrapper_fn = wrapper(fn, input_fn, output_fn)
    setattr(fn_module, fn.__name__, wrapper_fn)
    _replaced_functions[wrapper_fn] = (fn.__name__, fn)

