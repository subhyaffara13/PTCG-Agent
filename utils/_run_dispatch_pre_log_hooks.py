
def _run_dispatch_pre_log_hooks(call: "_DebugCall", func, types, args, kwargs) -> None:
    if _DISPATCH_PRE_LOG_HOOKS:
        for hook in _DISPATCH_PRE_LOG_HOOKS:
            hook_out = _run_hook(hook, func, types, args, kwargs, call)
            if hook_out is not None:
                # Store pre-hook results in call.log
                if call.log is None:
                    call.log = {}
                call.log.update(hook_out)

