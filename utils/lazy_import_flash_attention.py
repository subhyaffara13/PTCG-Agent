from typing import Callable

def lazy_import_flash_attention(
    implementation: str | None, attention_wrapper: Callable | None = None, allow_all_kernels: bool = False
):
    """
    Lazily import flash attention and return the respective functions + flags.

    NOTE: For fullgraph, this needs to be called before compile, while no fullgraph can
    work without preloading. See `load_and_register_attn_kernel` in `integrations.hub_kernels`.
    """
    global _loaded_implementation
    if implementation is None and _loaded_implementation is None:
        raise ValueError("Could not find any flash attn implementation based on your environment.")

    global _flash_fn, _flash_varlen_fn, _flash_with_kvcache_fn, _pad_fn, _unpad_fn, _process_flash_kwargs_fn
    if implementation is not None and _loaded_implementation != implementation:
        _loaded_implementation = implementation

        _flash_fn, _flash_varlen_fn, _flash_with_kvcache_fn, _pad_fn, _unpad_fn = _lazy_imports(
            implementation, attention_wrapper, allow_all_kernels=allow_all_kernels
        )
        # Block-sparse kernels register their own attention interface and expose no varlen fn to introspect;
        # skip building the kwargs-support map (it is only consumed by the flash varlen path they never take).
        _process_flash_kwargs_fn = _lazy_define_process_function(_flash_varlen_fn) if _flash_varlen_fn else None

    return (_flash_fn, _flash_varlen_fn, _flash_with_kvcache_fn, _pad_fn, _unpad_fn), _process_flash_kwargs_fn

