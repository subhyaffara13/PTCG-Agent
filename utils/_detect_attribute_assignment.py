
def _detect_attribute_assignment(mod: torch.nn.Module) -> Generator[None, None, None]:
    # Do not allow assignment of tensor attributes during export unless
    # the attribute is registered as a buffer.

    NN_MODULE_STD_ATTRS = [
        "_backward_hooks",
        "_backward_pre_hooks",
        "_buffers",
        "_forward_hooks",
        "_forward_hooks_always_called",
        "_forward_hooks_with_kwargs",
        "_forward_pre_hooks",
        "_forward_pre_hooks_with_kwargs",
        "_is_full_backward_hook",
        "_load_state_dict_post_hooks",
        "_load_state_dict_pre_hooks",
        "_modules",
        "_non_persistent_buffers_set",
        "_parameters",
        "_state_dict_hooks",
        "_state_dict_pre_hooks",
        "training",
    ]
    NN_MODULE_LAZY_STD_ATTRS = [
        "_initialize_hook",
        "_load_hook",
    ]
    STD_ATTRS = {
        *NN_MODULE_STD_ATTRS,
        *NN_MODULE_LAZY_STD_ATTRS,
    }

    def _get_attributes(mod: torch.nn.Module) -> dict[str, Any]:
        # return any attributes of a module that are not standard attributes
        return {k: v for k, v in mod.__dict__.items() if k not in STD_ATTRS}

    def _get_all_module_attributes(mod: torch.nn.Module) -> dict[str, dict[str, Any]]:
        # return attributes from all modules and submodules
        result = {}
        for name, submodule in mod.named_modules():
            result[name] = _get_attributes(submodule)
        return result

    def _restore_all_module_attributes(
        mod: torch.nn.Module, snapshot: dict[str, dict[str, Any]]
    ) -> None:
        # restore attributes to all modules and submodules
        for name, submodule in mod.named_modules():
            if name in snapshot:
                submodule.__dict__.update(snapshot[name])

    # save state of attributes before enter
    snapshot = pytree.tree_map(
        lambda x: x,
        _get_all_module_attributes(mod),
        is_leaf=lambda x: type(x) in _pytree_subclasses_that_lose_info,
    )
    try:
        yield
    finally:
        # after exit, compare state of attributes with snapshot
        # to detect which tensor attributes were assigned

        def _collect_assigned_tensor_attributes(
            snapshot: dict[str, dict[str, Any]], new_attrs: dict[str, dict[str, Any]]
        ) -> list[str]:
            assigned_tensor_attributes = []

            def _compare_values(path: str, old_val: Any, new_val: Any) -> None:
                """Recursively compare values, handling containers."""
                # Same object, no change
                if old_val is new_val:
                    return

                if old_val is None or new_val is None:
                    if isinstance(new_val, torch.Tensor):
                        assigned_tensor_attributes.append(path)
                    return

                # Check if it's a tensor that was reassigned
                if isinstance(new_val, torch.Tensor):
                    assigned_tensor_attributes.append(path)
                    return

                # Handle dict containers
                if isinstance(old_val, dict) and isinstance(new_val, dict):
                    all_keys = set(old_val.keys()) | set(new_val.keys())
                    for key in all_keys:
                        old_item = old_val.get(key)
                        new_item = new_val.get(key)
                        _compare_values(f"{path}[{key!r}]", old_item, new_item)
                    return

                # Handle list/tuple containers
                if isinstance(old_val, (list, tuple)) and isinstance(
                    new_val, (list, tuple)
                ):
                    # Different lengths = mutation happened
                    max_len = max(len(old_val), len(new_val))
                    for i in range(max_len):
                        old_item = old_val[i] if i < len(old_val) else None
                        new_item = new_val[i] if i < len(new_val) else None
                        _compare_values(f"{path}[{i}]", old_item, new_item)
                    return

                # For other types, just check if they're different objects
                # (we don't care about non-tensor mutations)

            for module_name in snapshot.keys() | new_attrs.keys():
                old_module_attrs = snapshot.get(module_name, {})
                new_module_attrs = new_attrs.get(module_name, {})

                for attr_name in old_module_attrs.keys() | new_module_attrs.keys():
                    module_prefix = f"self.{module_name}." if module_name else "self."
                    full_path = f"{module_prefix}{attr_name}"

                    old_val = old_module_attrs.get(attr_name)
                    new_val = new_module_attrs.get(attr_name)
                    _compare_values(full_path, old_val, new_val)

            return assigned_tensor_attributes

        new_attrs = _get_all_module_attributes(mod)
        assigned_tensor_attributes = _collect_assigned_tensor_attributes(
            snapshot, new_attrs
        )
        # restore state of all attributes (including, e.g., of primitive types)
        _restore_all_module_attributes(mod, snapshot)

        if assigned_tensor_attributes:
            if len(assigned_tensor_attributes) > 1:
                noun, verb = "attributes", "were"
            else:
                noun, verb = "attribute", "was"
            warnings.warn(
                f"The tensor {noun} {', '.join(assigned_tensor_attributes)} {verb} assigned during export. "
                "Such attributes must be registered as buffers using the `register_buffer` API "
                "(https://pytorch.org/docs/stable/generated/torch.nn.Module.html#torch.nn.Module.register_buffer).",
                stacklevel=2,
            )

