
def lazy_import_paged_flash_attention(implementation: str | None, allow_all_kernels: bool = False):
    """
    Same as `lazy_import_flash_attention` but explicitly wrapping it with the paged implementation.
    """
    from .integrations.flash_paged import paged_attention_forward

    (_, flash_attn_varlen_func, flash_attn_with_kvcache_fn, _, _), _ = lazy_import_flash_attention(
        implementation, attention_wrapper=paged_attention_forward, allow_all_kernels=allow_all_kernels
    )
    return flash_attn_varlen_func, flash_attn_with_kvcache_fn

