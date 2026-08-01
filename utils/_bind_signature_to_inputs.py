
def _bind_signature_to_inputs(mod, fake_args, fake_kwargs):
    if isinstance(mod, (torch.jit.ScriptModule, torch.jit.TracedModule)):
        sig = _get_torch_jit_trace_forward_signature(mod)

        # Sanity check for placeholder names coming from TorchScript.
        if len(sig.parameters) != len(fake_args) + len(fake_kwargs):
            raise AssertionError(
                "Arguments other than POSITIONAL_OR_KEYWORD kinds in forward() "
                "are not supported in _get_torch_jit_trace_forward_signature"
            )
    else:
        sig = inspect.signature(mod.forward)

    # Rather than binding both fake_args and fake_kwargs to sig names, we
    # (partially) bind only fake_args, while reusing fake_kwarg names. This
    # ensures that fake_kwargs do not get reordered, which is important to
    # match flattened user inputs.
    return {**sig.bind_partial(*fake_args).arguments, **fake_kwargs}

