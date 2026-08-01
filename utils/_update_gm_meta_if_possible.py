
def _update_gm_meta_if_possible(gm: torch.fx.GraphModule, mod: torch.nn.Module) -> None:
    if (
        isinstance(mod, torch.fx.GraphModule)
        and hasattr(mod, "meta")
        and "custom" in mod.meta
    ):
        gm.meta.update({"custom": mod.meta["custom"]})

