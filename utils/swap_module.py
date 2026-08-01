
def swap_module(
    mod, mapping, custom_module_class_mapping, use_precomputed_fake_quant=False
):
    r"""Swaps the module if it has a quantized counterpart and it has an
    `observer` attached.

    Args:
        mod: input module
        mapping: a dictionary that maps from nn module to nnq module

    Return:
        The corresponding quantized module of `mod`
    """
    new_mod = mod
    if hasattr(mod, "qconfig") and mod.qconfig is not None:
        swapped = False
        if type_before_parametrizations(mod) in custom_module_class_mapping:
            new_mod = custom_module_class_mapping[
                type_before_parametrizations(mod)
            ].from_observed(mod)
            swapped = True
        elif type_before_parametrizations(mod) in mapping:
            qmod = mapping[type_before_parametrizations(mod)]
            if hasattr(qmod, "_IS_REFERENCE") and qmod._IS_REFERENCE:
                if mod.qconfig is None:
                    raise AssertionError(
                        "module qconfig must not be None when swapping to reference module"
                    )
                weight_post_process = mod.qconfig.weight()
                weight_post_process(mod.weight)
                weight_qparams = get_qparam_dict(weight_post_process)
                new_mod = qmod.from_float(mod, weight_qparams)
            else:
                sig = inspect.signature(qmod.from_float)
                if "use_precomputed_fake_quant" in sig.parameters:
                    new_mod = qmod.from_float(
                        mod, use_precomputed_fake_quant=use_precomputed_fake_quant
                    )
                else:
                    new_mod = qmod.from_float(mod)
            swapped = True

        if swapped:
            # Preserve module's pre forward hooks. They'll be called on quantized input
            for pre_hook_fn in mod._forward_pre_hooks.values():
                new_mod.register_forward_pre_hook(pre_hook_fn)
            # Preserve module's post forward hooks except _observer_forward_hook
            # After convert they'll work with quantized output
            for hook_fn in mod._forward_hooks.values():
                if hook_fn is not _observer_forward_hook:
                    new_mod.register_forward_hook(hook_fn)

            # respect device affinity when swapping modules
            devices = _get_unique_devices_(mod)
            if not (
                len(devices) <= 1
                or (len(devices) == 2 and torch.device("meta") in devices)
            ):
                raise AssertionError(
                    f"swap_module only works with cpu or single-device CUDA modules, but got devices {devices}"
                )
            device = next(iter(devices)) if len(devices) > 0 else None
            if device:
                new_mod.to(device)
    return new_mod


def swap_module(
    mod: nn.Module, mapping: dict[type[nn.Module], type[nn.Module]]
) -> nn.Module:
    r"""Swaps the module using from_dense according to the mapping passed in.
    Args:
        mod: input module
        mapping: a dictionary that maps from nn module to sparse nn module
    Return:
        The corresponding sparse module of `mod` according to mapping, created using from_dense
    """
    if type_before_parametrizations(mod) in mapping:
        sparse_mod = mapping[type_before_parametrizations(mod)]

        # TODO Fix this typing, as Type[Module] has no attribute "from_dense"
        new_mod = sparse_mod.from_dense(mod)  # type: ignore[attr-defined]

        # Preserve module's pre forward hooks. They'll be called on quantized input
        for pre_hook_fn in mod._forward_pre_hooks.values():
            new_mod.register_forward_pre_hook(pre_hook_fn)
        # Preserve module's post forward hooks except _observer_forward_hook
        # After convert they'll work with quantized output
        for hook_fn in mod._forward_hooks.values():
            new_mod.register_forward_hook(hook_fn)

        # respect device affinity when swapping modules
        # pyrefly: ignore [bad-argument-type]
        devices = {p.device for p in chain(mod.parameters(), mod.buffers())}
        if len(devices) > 1:
            raise AssertionError(
                f"swap_module only works with cpu or single-device CUDA modules, but got devices {devices}"
            )
        device = next(iter(devices)) if len(devices) > 0 else None
        if device:
            new_mod.to(device)

        return new_mod

    else:
        return mod

