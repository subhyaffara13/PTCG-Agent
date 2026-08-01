
def make_parent_class_for_kernel_fusion(
    parent_cls: type,
    child_names: list[str],
    kernel_cls: type,
) -> type:
    """
    Create a new class that inherits from `parent_cls` and fuses the child modules specified in `child_names
    with the provided `kernel_cls`.
    The first child in `child_names` will be replaced with the `kernel_cls`, and the rest will be replaced with
    `nn.Identity()` to keep the same interface.
    """
    original_init = parent_cls.__init__

    def patched_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        children = [getattr(self, name) for name in child_names]
        kernel_instance = kernel_cls(*children)
        setattr(self, child_names[0], kernel_instance)
        for name in child_names[1:]:
            setattr(self, name, nn.Identity())

    patched_cls = type(f"Fused{parent_cls.__name__}", (parent_cls,), {"__init__": patched_init})
    patched_cls.__qualname__ = f"Fused{parent_cls.__qualname__}"
    return patched_cls

