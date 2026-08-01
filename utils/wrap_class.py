
def wrap_class(
    cls: type[object],
    cls_sourceinfo: str | None,
) -> type[object]:
  class WrappedClass:

    @util.wraps(cls.__init__)
    def __init__(self, *init_args, **init_kwargs) -> None:
      uid = self._colocated_python_uid = (
          SINGLETON_INSTANCE_REGISTRY.new_instance()
      )
      self.func_maker = func._CachedColocatedFunctionMaker(uid)
      for attr_name in dir(cls):
        original_member = getattr(cls, attr_name)
        if not inspect.isfunction(original_member):
          continue

        # WrappedClass defines lazy initialization and colocated deletion logic.
        # WrappedClass is not serializable even if the original class may be
        # serializable.
        if attr_name in ('__init__', '__del__', '__reduce__', '__reduce_ex__'):
          continue

        method = _make_method(
            cls,
            cls_sourceinfo,
            uid,
            init_args,
            init_kwargs,
            attr_name,
            original_member,
            self.func_maker,
        )
        # TODO(hyeontaek): Support method specialization similar to function
        # specialization.
        setattr(self, attr_name, method)

  WrappedClass.__name__ = cls.__name__
  WrappedClass.__doc__ = cls.__doc__
  return WrappedClass

