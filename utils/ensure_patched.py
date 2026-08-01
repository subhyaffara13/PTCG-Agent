
def ensure_patched(cls: Any) -> None:
    if getattr(cls, "___needs_mutation_patch", True):
        cls.___needs_mutation_patch = False
        original_setattr = cls.__setattr__

        @functools.wraps(original_setattr)
        def custom_setattr(self: Any, key: str, value: Any) -> None:
            try:
                MutationTracker.db[self].on_mutation(key)
            except KeyError:
                pass
            return original_setattr(self, key, value)

        cls.__setattr__ = custom_setattr

