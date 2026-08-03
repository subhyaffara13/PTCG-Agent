from typing import Any

def compile_mps_shaders(
    kernels: list[tuple[str, str, list[str]]],
) -> dict[str, Any]:
    """Compile a batch of Metal kernels into one library.

    Args:
        kernels: list of (kernel_name, metal_source, headers) tuples.
            headers are bare names resolved as <c10/metal/{name}.h>.

    Returns:
        dict mapping each kernel_name to its compiled function handle.
    """
    from torch.utils._ordered_set import OrderedSet

    all_headers = sorted(OrderedSet(h for _, _, hs in kernels for h in hs))
    header_src = "\n".join(f"#include <c10/metal/{h}.h>" for h in all_headers)
    body_src = "\n".join(src for _, src, _ in kernels)
    lib = compile_mps_shader(header_src + "\n" + body_src)
    return {name: getattr(lib, name) for name, _, _ in kernels}

