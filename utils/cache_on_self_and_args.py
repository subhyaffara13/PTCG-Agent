
def cache_on_self_and_args(
    class_name: str,
) -> Callable[[FN_TYPE[P, RV]], FN_TYPE[P, RV]]:
    # include both class_name and fn_name in the key to support `super().fn(self, **args, **kwargs)` calls.

    def wrapper(
        fn: FN_TYPE[P, RV],
    ) -> FN_TYPE[P, RV]:
        key = f"__{class_name}_{fn.__name__}_cache"

        # wrapper is likely on the hot path, compile a specialized version of it
        ctx = {"fn": fn}
        exec(
            f"""\
            def inner(self: Any, *args: P.args, **kwargs: P.kwargs) -> RV:
                args_kwargs = (args, tuple(sorted(kwargs.items())))

                if not hasattr(self, "{key}"):
                    object.__setattr__(self, "{key}", {{}})

                cache = self.{key}

                try:
                    return cache[args_kwargs]
                except KeyError:
                    pass

                rv = fn(self, *args, **kwargs)

                cache[args_kwargs] = rv
                return rv
            """.lstrip(),
            ctx,
        )
        inner = functools.wraps(fn)(ctx["inner"])

        def clear_cache(self: Any) -> None:
            if hasattr(self, key):
                delattr(self, key)

        inner.clear_cache = clear_cache  # type: ignore[attr-defined]
        return inner

    return wrapper

