from typing import Callable

def _post_order_apply(
    root_module: nn.Module,
    fn: Callable[[nn.Module], nn.Module | None],
):
    """
    This applies ``fn`` to every module in the module tree of ``root_module``
    following a post-order traversal. If ``fn`` returns an :class:`nn.Module`,
    then this replaces the original module with the newly returned one in the
    tree. Otherwise, ``fn`` should return ``None``, in which case the module is
    not changed.
    """
    # Track visited modules to avoid visiting shared modules multiple times
    visited_modules: set[nn.Module] = {root_module}

    def _post_order_apply_inner(
        module: nn.Module,
        module_name: str,
        parent_module: nn.Module | None,
    ):
        for child_module_name, child_module in module.named_children():
            if child_module not in visited_modules:
                visited_modules.add(child_module)
                _post_order_apply_inner(child_module, child_module_name, module)
        optional_module = fn(module)
        if optional_module is not None:
            if not isinstance(parent_module, nn.Module):
                raise AssertionError(
                    "Non-root modules should have their parent module set but got "
                    f"{parent_module} for {module}"
                )
            if not module_name:
                raise AssertionError(
                    "Non-root modules should have their module name set but got "
                    f"an empty module name for {module}"
                )
            if not isinstance(optional_module, nn.Module):
                raise AssertionError(
                    f"fn should return None or an nn.Module but got {optional_module}"
                )
            setattr(parent_module, module_name, optional_module)

    _post_order_apply_inner(root_module, "", None)

