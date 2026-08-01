
def _make_temp_remove_mode_context_manager(
    mode_ty: type[TorchFunctionMode],
) -> Callable[[], _GeneratorContextManager[TorchFunctionMode | None]]:
    @contextmanager
    def context_manager_fn() -> Generator[TorchFunctionMode | None, None, None]:
        from torch.overrides import _len_torch_function_stack, _pop_mode, _push_mode

        temp_elements = []
        removed_mode = None

        while _len_torch_function_stack() > 0:
            mode = _pop_mode()
            if isinstance(mode, mode_ty):
                removed_mode = mode
                break
            else:
                temp_elements.append(mode)

        for mode in reversed(temp_elements):
            _push_mode(mode)

        try:
            yield removed_mode

        finally:
            if removed_mode is not None:
                count = len(temp_elements)
                while count > 0:
                    mode = _pop_mode()
                    count -= 1

                temp_elements.append(removed_mode)

                for mode in reversed(temp_elements):
                    _push_mode(mode)

    return context_manager_fn

