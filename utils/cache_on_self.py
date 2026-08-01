
def cache_on_self(fn: Callable[Concatenate[Any, P], RV]) -> CachedMethod[P, RV]:
    name = fn.__name__
    key = f"__{name}_cache"

    # wrapper is likely on the hot path, compile a specialized version of it
    ctx = {"fn": fn}
    exec(
        f"""\
        def {name}_cache_on_self(self):
            try:
                return self.{key}
            except AttributeError:
                pass
            rv = fn(self)
            object.__setattr__(self, "{key}", rv)
            return rv
        """.lstrip(),
        ctx,
    )
    wrapper = functools.wraps(fn)(ctx[f"{name}_cache_on_self"])

    def clear_cache(self: Any) -> None:
        if hasattr(self, key):
            delattr(self, key)

    wrapper.clear_cache = clear_cache  # type: ignore[attr-defined]
    return wrapper  # type: ignore[return-value]

