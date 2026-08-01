
def _apply_to_module(
    modules: tuple[nn.Module, ...],
    cls_to_wrapper_cls: dict[type, type],
    wrapper_module_cls: type,
    wrapper_cls_prefix: str,
    unimplemented_deepcopy: "Callable",
) -> None:
    """
    Modify module classes to include the wrapper class in their MRO.

    Args:
        modules: The modules to apply the wrapper to.
        cls_to_wrapper_cls: Cache dict mapping original class to wrapper class.
        wrapper_module_cls: The wrapper module class (e.g., FSDPModule, ReplicateModule).
        wrapper_cls_prefix: Prefix for the dynamically created class name (e.g., "FSDP", "Replicate").
        unimplemented_deepcopy: The deepcopy function to use for the wrapper class.
    """
    for module in modules:
        cls = module.__class__
        new_cls = cls_to_wrapper_cls.get(cls)
        if not new_cls:
            dct = {"__deepcopy__": unimplemented_deepcopy}
            new_cls = type(
                f"{wrapper_cls_prefix}{cls.__name__}", (wrapper_module_cls, cls), dct
            )
            cls_to_wrapper_cls[cls] = new_cls
        module.__class__ = new_cls

