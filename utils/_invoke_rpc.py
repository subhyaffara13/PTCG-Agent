
def _invoke_rpc(
    to, func, rpc_type, args=None, kwargs=None, rpc_timeout: float = UNSET_RPC_TIMEOUT
):
    if not callable(func):
        raise TypeError("function should be callable.")

    qualified_name = torch.jit._builtins._find_builtin(func)
    dst_worker_info = _to_worker_info(to)

    should_profile = _get_should_profile()

    ctx_manager = _enable_rpc_profiler(
        should_profile, qualified_name, func, rpc_type, dst_worker_info
    )

    with ctx_manager as rf:
        args = args if args else ()
        kwargs = kwargs if kwargs else {}

        is_async_exec = hasattr(func, "_wrapped_async_rpc_function")

        if is_async_exec:
            # pyrefly: ignore [missing-attribute]
            wrapped = func._wrapped_async_rpc_function
            if isinstance(wrapped, torch.jit.ScriptFunction):
                func = wrapped

        if qualified_name is not None:
            fut = _invoke_rpc_builtin(
                dst_worker_info, qualified_name, rpc_timeout, *args, **kwargs
            )
        elif isinstance(func, torch.jit.ScriptFunction):
            fut = _invoke_rpc_torchscript(
                dst_worker_info.name,
                torch._jit_internal._qualified_name(func),
                args,
                kwargs,
                rpc_timeout,
                is_async_exec,
            )
        else:
            (pickled_python_udf, tensors) = _default_pickler.serialize(
                PythonUDF(func, args, kwargs)
            )
            fut = _invoke_rpc_python_udf(
                dst_worker_info, pickled_python_udf, tensors, rpc_timeout, is_async_exec
            )
        if should_profile:
            if not torch.autograd._profiler_enabled():
                raise AssertionError
            if rf is None:
                raise AssertionError
            # Schedule profiling callbacks to run when the future completes.
            # This returns a future that is completed when the original future
            # completes and the profiling callbacks have been completed as well,
            # to guarantee that fut.wait() completes the profiling. This new
            # future will contain the same value as the original future.
            fut = rf._call_end_callbacks_on_future(fut)
    return fut


def _invoke_rpc(rref, rpc_api, func_name, timeout, *args, **kwargs):
    def _rref_type_cont(rref_fut):
        rref_type = rref_fut.value()

        _invoke_func = _local_invoke
        # Bypass ScriptModules when checking for async function attribute.
        bypass_type = issubclass(rref_type, torch.jit.ScriptModule) or issubclass(
            rref_type, torch._C.ScriptModule
        )
        if not bypass_type:
            func = getattr(rref_type, func_name)
            if hasattr(func, "_wrapped_async_rpc_function"):
                _invoke_func = _local_invoke_async_execution

        return rpc_api(
            rref.owner(),
            _invoke_func,
            args=(rref, func_name, args, kwargs),
            timeout=timeout,
        )

    rref_fut = rref._get_type(timeout=timeout, blocking=False)

    if rpc_api is not rpc_async:
        rref_fut.wait()
        return _rref_type_cont(rref_fut)
    else:
        # A little explanation on this.
        # rpc_async returns a Future pointing to the return value of `func_name`, it returns a `Future[T]`
        # Calling _rref_type_cont from the `then` lambda causes Future wrapping. IOW, `then` returns a `Future[Future[T]]`
        # To address that, we return a Future that is completed with the result of the async call.
        result: Future = Future()

        def _wrap_rref_type_cont(fut):
            try:
                _rref_type_cont(fut).then(_complete_op)
            except BaseException as ex:  # noqa: B036
                result.set_exception(ex)

        def _complete_op(fut):
            try:
                result.set_result(fut.value())
            except BaseException as ex:  # noqa: B036
                result.set_exception(ex)

        rref_fut.then(_wrap_rref_type_cont)
        return result

