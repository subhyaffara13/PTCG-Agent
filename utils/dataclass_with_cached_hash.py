from typing import Any, Callable

def dataclass_with_cached_hash(cls: type[T], **kwargs: Any) -> type[T]: ...


def dataclass_with_cached_hash(
    cls: None = None, **kwargs: Any
) -> Callable[[type[T]], type[T]]: ...


def dataclass_with_cached_hash(
    cls: type[T] | None = None, **kwargs: Any
) -> type[T] | Callable[[type[T]], type[T]]:
    def wrap(cls_inner: type[T]) -> type[T]:
        new_cls = dataclasses.dataclass(cls_inner, **kwargs)
        old_hash = cls_inner.__hash__

        def __hash__(self) -> int:
            if not hasattr(self, "_hash"):
                object.__setattr__(self, "_hash", old_hash(self))
            return self._hash

        def __reduce__(self):
            # Exclude _hash from pickling to ensure deterministic cache keys.
            # The _hash is a cached value that can be nondeterministically computed
            # (e.g., based on id() of objects), so it should not affect pickling.
            fields = dataclasses.fields(self)
            field_values = tuple(getattr(self, f.name) for f in fields if f.init)
            return (self.__class__, field_values)

        new_cls.__hash__ = __hash__
        new_cls.__reduce__ = __reduce__
        return new_cls  # type: ignore[return-value]

    if cls is None:
        return wrap

    return wrap(cls)

