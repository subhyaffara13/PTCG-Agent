
def _allow_in_graph_einops() -> None:
    import einops

    # There is a lru_cache logspam issue with einops when allow_in_graph is not
    # used. Disabling this for now until the lru_cache issue is resolved.
    # if einops.__version__ >= "0.8.2":
    #     if hasattr(einops, "einops") and hasattr(einops.einops, "get_backend"):
    #         # trigger backend registration up front to avoid a later guard failure
    #         # that would otherwise cause a recompilation
    #         einops.rearrange(torch.randn(1), "i -> i")
    #     # einops 0.8.2+ don't need explicit allow_in_graph calls
    #     return

    try:
        # requires einops > 0.6.1, torch >= 2.0
        from einops._torch_specific import (  # type: ignore[attr-defined]  # noqa: F401
            _ops_were_registered_in_torchdynamo,
        )

        # einops > 0.6.1 will call the op registration logic as it is imported.
    except ImportError:
        # einops <= 0.6.1 doesn't handle unhashable SymInt in its lru_cache'd
        # helpers. Backport the try/except TypeError fallback from einops 0.7.0+
        # so allow_in_graph works during fake tensor validation.
        _patch_einops_symint_compat(einops.einops)  # type: ignore[attr-defined]
        allow_in_graph(einops.rearrange)
        allow_in_graph(einops.reduce)
        if hasattr(einops, "repeat"):
            allow_in_graph(einops.repeat)  # available since einops 0.2.0
        if hasattr(einops, "einsum"):
            allow_in_graph(einops.einsum)  # available since einops 0.5.0
        if hasattr(einops, "pack"):
            allow_in_graph(einops.pack)  # available since einops 0.6.0
        if hasattr(einops, "unpack"):
            allow_in_graph(einops.unpack)  # available since einops 0.6.0

