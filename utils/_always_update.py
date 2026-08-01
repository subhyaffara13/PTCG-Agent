
def _always_update(f: F) -> F:
    def wrapper(
        self: UpdateDictMixin[t.Any, t.Any], /, *args: t.Any, **kwargs: t.Any
    ) -> t.Any:
        rv = f(self, *args, **kwargs)

        if self.on_update is not None:
            self.on_update(self)

        return rv

    return update_wrapper(wrapper, f)  # type: ignore[return-value]

