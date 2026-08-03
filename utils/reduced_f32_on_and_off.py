import functools

def reduced_f32_on_and_off(bf32_precision=1e-2, tf32_precision=1e-5):
    def with_reduced_f32_disabled(self, function_call):
        with reduced_f32_off():
            function_call()

    def with_bf32_enabled(self, function_call):
        with bf32_on(self, bf32_precision):
            function_call()

    def with_tf32_enabled(self, function_call):
        with tf32_on(self, tf32_precision):
            function_call()

    def wrapper(f):
        params = inspect.signature(f).parameters
        arg_names = tuple(params.keys())

        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            kwargs.update(zip(arg_names, args, strict=False))
            cond = True
            if "device" in kwargs:
                cond = cond and (torch.device(kwargs["device"]).type == "cpu")
            if "dtype" in kwargs:
                cond = cond and (kwargs["dtype"] == torch.float)
            bf32_cond = cond and bf32_is_not_fp32()
            tf32_cond = cond and tf32_is_not_fp32()
            if bf32_cond or tf32_cond:
                with_reduced_f32_disabled(kwargs["self"], lambda: f(**kwargs))
                if bf32_cond:
                    with_bf32_enabled(kwargs["self"], lambda: f(**kwargs))
                if tf32_cond:
                    with_tf32_enabled(kwargs["self"], lambda: f(**kwargs))
            else:
                f(**kwargs)

        return wrapped

    return wrapper

