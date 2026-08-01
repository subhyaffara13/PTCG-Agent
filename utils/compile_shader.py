
def compile_shader(source: str):
    r"""Compiles compute shader from source and allows one to invoke kernels
    defined there from the comfort of Python runtime
    Example::

        >>> # xdoctest: +REQUIRES(env:TORCH_DOCTEST_MPS)
        >>> lib = torch.mps.compile_shader(
        ... "kernel void full(device float* out, constant float& val, uint idx [[thread_position_in_grid]]) { out[idx] = val; }"
        ...  )
        >>> x = torch.zeros(16, device="mps")
        >>> lib.full(x, 3.14)
    """
    from pathlib import Path

    from torch.utils._cpp_embed_headers import _embed_headers

    if not hasattr(torch._C, "_mps_compileShader"):
        raise RuntimeError("MPS is not available")
    source = _embed_headers(
        [l + "\n" for l in source.split("\n")],
        [Path(__file__).parent.parent / "include"],
        set(),
    )
    return torch._C._mps_compileShader(source)

