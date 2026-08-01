
def _get_cpp_wrapper_header(device: str, aot_mode: bool = False) -> str:
    """Given a device type (and optionally whether we're in AOT Inductor mode), returns
    the path to the cpp_wrapper header file to be precompiled."""
    base_device = device.split(":", maxsplit=1)[0]
    is_array_ref = config.aot_inductor.allow_stack_allocation and base_device == "cpu"
    return (
        "torch/csrc/inductor/"
        f"{'aoti_include' if aot_mode else 'cpp_wrapper'}/"
        f"{'array_ref' if is_array_ref else base_device}.h"
    )

