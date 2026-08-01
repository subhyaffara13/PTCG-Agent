
def _collect_context_fn_hashes(gm: torch.fx.GraphModule) -> list[str]:
    """
    Collect cache hashes from all context_fn used in SAC HOPs within the graph module.

    Returns a list of hashes. Raises BypassAOTAutogradCache if any context_fn
    lacks a cache_hash attribute.
    """
    hashes = []
    for module in gm.modules():
        if not isinstance(module, torch.fx.GraphModule):
            continue
        context_fn = module.meta.get("_checkpoint_context_fn")
        if context_fn is not None:
            cache_hash = _get_context_fn_cache_hash(context_fn)
            if cache_hash is None:
                raise BypassAOTAutogradCache(
                    "SAC context_fn does not have a cache_hash attribute. "
                    "To enable caching with selective activation checkpointing, "
                    "add a 'cache_hash' attribute to your context_fn. This can be "
                    "a string or any hashable value that uniquely identifies the checkpointing "
                    "behavior (e.g., based on source code hash and closed-over globals). "
                    "For functools.partial objects, set cache_hash on the partial itself."
                )
            hashes.append(cache_hash)
    return hashes

