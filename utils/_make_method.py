
def _make_method(
    cls: type[object],
    cls_sourceinfo: str | None,
    uid: int,
    init_args: tuple[Any, ...],
    init_kwargs: dict[str, Any],
    method_name: str,
    original_method: Callable[..., Any],
    func_maker: func._CachedColocatedFunctionMaker,
):

  class MethodCallerAtBackend:

    def __init__(self):
      self._lock = threading.Lock()

    def __reduce__(self):
      return type(self), ()

    def _first_call(self):
      def initializer():
        return obj_backend._ConsumableRef(cls(*init_args, **init_kwargs))

      retrieved = obj_backend.SINGLETON_OBJECT_STORE.get_or_create(
          uid, initializer
      )

      self.obj = retrieved()

    def __call__(self, *args, **kwargs):
      with self._lock:
        if not hasattr(self, 'obj'):
          self._first_call()

      return getattr(self.obj, method_name)(*args, **kwargs)

    def __del__(self):
      if not hasattr(self, 'obj'):
        # It is possible that no one has ever consumed the _ConsumableRef. So
        # consume it now.
        obj_backend.SINGLETON_OBJECT_STORE.get_or_create(
            uid, lambda: obj_backend._ConsumableRef(None)
        )()

  # Colocated Python callable for the controller.
  callable = func_maker.make_callable(
      MethodCallerAtBackend(),
      cls_sourceinfo,
      api_util.fun_signature(original_method),
  )

  # Outer wrapper of the method for the controller. It tracks devices that have
  # been used with any method call.
  def make_method_wrapper(callable):
    @api_boundary
    def method_wrapper(*args, **kwargs):
      # TODO(hyeontaek): Instead of inspecting argument/result shardings, get
      # shardings from final specialization of the function. This may require
      # lowering `_update_instance_devices` into the function API.

      args_leaves = tree_util.tree_leaves((args, kwargs))
      args_shardings_leaves = tuple(
          func._get_spec(x).sharding for x in args_leaves
      )
      if args_shardings_leaves:
        _update_instance_devices(uid, args_shardings_leaves)

      result = callable(*args, **kwargs)

      # If args had any array, we can skip incorporating devices from the result
      # because results will not use any new devices.
      if not args_shardings_leaves:
        result_leaves = tree_util.tree_leaves(result)
        result_shardings_leaves = tuple(
            func._get_spec(x).sharding for x in result_leaves
        )
        _update_instance_devices(uid, result_shardings_leaves)
      return result

    def specialize(*args, **kwargs):
      return make_method_wrapper(callable.specialize(*args, **kwargs))

    method_wrapper = util.wraps(original_method)(method_wrapper)
    method_wrapper.specialize = specialize  # pyrefly: ignore[missing-attribute]
    return method_wrapper

  method_wrapper = make_method_wrapper(callable)
  return method_wrapper

