import os

def patch_torch_compile_force_graph():
    """
    Patch `torch.compile` to always use `fullgraph=True`.

    This is useful when some `torch.compile` tests are running with `fullgraph=False` and we want to be able to run
    them with `fullgraph=True` in some occasion (without introducing new tests) to make sure there is no graph break.

    After PR #40137, `CompileConfig.fullgraph` is `False` by default, this patch is necessary.
    """

    force_fullgraph = os.environ.get("TORCH_COMPILE_FORCE_FULLGRAPH", "")
    force_fullgraph = force_fullgraph.lower() in ("yes", "true", "on", "t", "y", "1")

    if force_fullgraph:
        import torch

        orig_method = torch.compile

        def patched(*args, **kwargs):
            # In `torch_compile`, all arguments except `model` is keyword only argument.
            kwargs["fullgraph"] = True
            return orig_method(*args, **kwargs)

        torch.compile = patched

