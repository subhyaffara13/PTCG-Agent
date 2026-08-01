
def discard_traced_gm_params(mod: torch.fx.GraphModule):
    with torch.utils._python_dispatch._disable_current_modes():
        for attr_name, tensor in list(
            itertools.chain(
                mod.named_parameters(recurse=False),
                # pyrefly: ignore [bad-argument-type]
                mod.named_buffers(recurse=False),
            )
        ):
            with torch._dispatch.python.no_python_dispatcher():
                e_t = ErasedTensor(tensor, attr_name, mod)
            if isinstance(tensor, torch.nn.Parameter):
                e_t.requires_grad_(True)
                e_t._is_param = True
            setattr(mod, attr_name, e_t)

