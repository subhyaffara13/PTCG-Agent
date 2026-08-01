
def _disable_remat_for_regional_subcompile() -> Iterator[None]:
    # In torch.compile, regional_inductor subcompiles run after the enclosing
    # non-strict full graph has already been partitioned, so any graph-SAC
    # remat pass has already run before we reach this nested compile.
    # Rerunning remat here can see stage-2-reordered backward nodes that
    # violate remat's contiguous-backward-region assumption.
    with torch._functorch.config.patch(remat_using_tags_for_fwd_loss_bwd_graph=False):
        yield

