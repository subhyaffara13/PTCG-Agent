
def _get_cpp_prefix_header(device: str) -> str | None:
    if device.startswith("cpu"):
        return "torch/csrc/inductor/cpp_prefix.h"
    return None

