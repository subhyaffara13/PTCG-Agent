
def _disable_context_parallel_dispatcher_impl() -> None:
    if _dispatch_mode == _DispatchMode.MONKEY_PATCH:
        _restore_function(F.scaled_dot_product_attention, F)
    elif _dispatch_mode == _DispatchMode.MODULE_WRAPPER:
        pass
    else:
        raise NotImplementedError(f"Unknown dispatch mode: {_dispatch_mode}")

    _disable_cp_dtensor_dispatcher()

