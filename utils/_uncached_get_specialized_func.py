
def _uncached_get_specialized_func(
    info: FunctionInfo,
    specialization: Specialization,
) -> Callable[..., Any]:
  """Returns a specialized function for the given specialization."""
  util.test_event("colocated_python_func._get_specialized_func")
  assert specialization.in_specs_treedef is not None
  assert specialization.in_specs_leaves is not None
  assert specialization.devices is not None
  uid = random.getrandbits(63)

  mutex = threading.Lock()
  # Asynchronous execution function that has known output_specs.
  async_execution_func = None

  def specialized_func(*args, **kwargs):
    """Specialized function to be executed with given args and kwargs."""
    nonlocal specialization, async_execution_func
    with mutex:
      if async_execution_func is None:
        if specialization.out_specs_treedef is None:
          if specialization.out_specs_fn is None:
            output_specs_and_push_result_fun = (
                _make_output_specs_and_push_result_fun(
                    info, specialization, uid
                )
            )
            serialized_out_specs = output_specs_and_push_result_fun(
                *args, **kwargs
            )

            # Waits for the output_specs. This may block.
            out_specs_treedef, out_specs_leaves = _deserialize_specs(
                serialized_out_specs
            )

            # Subsequent calls would use async_execution_func with discovered
            # output_specs.
            specialization = specialization.update(
                out_specs_treedef=out_specs_treedef,
                out_specs_leaves=out_specs_leaves,
            )
            async_execution_func = _make_async_execution_fun(
                info, specialization
            )

            # Hold the PyExecutable until async_execution_fun is called at
            # least once, so the number of _OBJECT_STORE references at the
            # backend does not drop to 0.
            async_execution_func.output_specs_and_push_result_fun = (  # pyrefly: ignore[missing-attribute]
                output_specs_and_push_result_fun
            )

            return _make_pop_result_fun(info, specialization, uid)()
          else:
            # Compute out_specs using out_specs_fn and inputs.
            args_specs, kwargs_specs = tree_util.tree_map(
                _get_spec, (args, kwargs)
            )
            out_specs = specialization.out_specs_fn(*args_specs, **kwargs_specs)
            out_specs_leaves, out_specs_treedef = tree_util.tree_flatten(
                out_specs
            )
            specialization = specialization.update(
                out_specs_treedef=out_specs_treedef,
                out_specs_leaves=tuple(out_specs_leaves),
            )
            async_execution_func = _make_async_execution_fun(
                info, specialization
            )
            # Fall-through.
        else:
          async_execution_func = _make_async_execution_fun(info, specialization)
          # Fall-through.

    # Asynchronous execution runs outside of the mutex to allow concurrent
    # execution for inline executors.
    result = async_execution_func(*args, **kwargs)
    with mutex:
      async_execution_func.output_specs_and_push_result_fun = None  # pyrefly: ignore[missing-attribute]
    return result

  return specialized_func

