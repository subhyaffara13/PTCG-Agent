
def _maybe_fake_prop_ignore_unbacked(fn, args):
    with suspend_functionalization(), disable_functional_mode():
        with disable_proxy_modes_tracing():
            unfunc_args = [_from_fun(arg) for arg in args]
        with ExitStack() as ctx_stack:
            ctx_stack.enter_context(
                torch.utils._python_dispatch._disable_current_modes()
            )
            if (fake_mode := detect_fake_mode(unfunc_args)) is not None:
                ctx_stack.enter_context(fake_mode)
                if fake_mode.shape_env is not None:
                    ctx_stack.enter_context(
                        fake_mode.shape_env.ignore_fresh_unbacked_symbols()
                    )
            return fn(*unfunc_args)

