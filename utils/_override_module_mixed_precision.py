from typing import Any

def _override_module_mixed_precision(
    root: torch.nn.Module,
    module_classes_to_override: Iterable[type[nn.Module]],
    wrap_override_dict: dict[str, Any] = {"mixed_precision": None},  # noqa: B006
) -> set[type[nn.Module]]:
    module_classes_to_override = tuple(set(module_classes_to_override))
    # Return a set of the actually overridden module classes
    overridden_module_classes: set[type[nn.Module]] = set()
    for mod in root.modules():
        if isinstance(mod, module_classes_to_override):
            overridden_module_classes.add(type(mod))
            mod._wrap_overrides = wrap_override_dict  # type: ignore[assignment]
            # TODO: We need to run this mixed precision ignored module in fp32,
            # but ensure subsequent modules, that may possibly be running with
            # mixed precision, still receive the appropriate precision inputs
            # without user having to adjust mixed precision config too much.
            # As a result, we attach pre and post forward hooks to up / down
            # cast. We should revisit this design.

            def cast_fn(
                dtype: torch.dtype, module: nn.Module, x: torch.Tensor
            ) -> torch.Tensor:
                if not torch.is_floating_point(x) or x.dtype == dtype:
                    return x
                _MODULE_TO_INP_DTYPE[module] = x.dtype
                return x.to(dtype)

            def forward_pre_hook(module, args):
                return _apply_to_tensors(partial(cast_fn, torch.float32, module), args)

            def forward_post_hook(module, args, output):
                # NOTE: If the forward did not have any floating-point tensors,
                # then the dtype will not be set for this module, and we do not
                # upcast the dtype.
                if module in _MODULE_TO_INP_DTYPE:
                    old_dtype = _MODULE_TO_INP_DTYPE[module]
                    return _apply_to_tensors(
                        partial(cast_fn, old_dtype, module), output
                    )

            # We intentionally append both of these hooks so that they run after
            # all other hooks.
            mod.register_forward_pre_hook(forward_pre_hook, prepend=False)
            mod.register_forward_hook(forward_post_hook, prepend=False)
    return overridden_module_classes

