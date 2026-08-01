
def _wrap_module_cls_individually(
    module: nn.Module, module_classes: Sequence[type], recurse: bool, *args, **kwargs
):
    if recurse:
        # always recurse
        return True
    else:
        # if not recursing, decide whether we should wrap based on whether the type of module
        # is in `module_classes`.
        return isinstance(module, tuple(module_classes))

