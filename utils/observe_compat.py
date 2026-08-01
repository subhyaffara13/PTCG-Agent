
def observe_compat(func: FuncT) -> FuncT:
    """Backward-compatibility shim decorator for observers

    Use with:

    @observe('name')
    @observe_compat
    def _foo_changed(self, change):
        ...

    With this, `super()._foo_changed(self, name, old, new)` in subclasses will still work.
    Allows adoption of new observer API without breaking subclasses that override and super.
    """

    def compatible_observer(
        self: t.Any, change_or_name: str, old: t.Any = Undefined, new: t.Any = Undefined
    ) -> t.Any:
        if isinstance(change_or_name, dict):  # type:ignore[unreachable]
            change = Bunch(change_or_name)  # type:ignore[unreachable]
        else:
            clsname = self.__class__.__name__
            warn(
                f"A parent of {clsname}._{change_or_name}_changed has adopted the new (traitlets 4.1) @observe(change) API",
                DeprecationWarning,
                stacklevel=2,
            )
            change = Bunch(
                type="change",
                old=old,
                new=new,
                name=change_or_name,
                owner=self,
            )
        return func(self, change)

    return compatible_observer  # type:ignore[return-value]

