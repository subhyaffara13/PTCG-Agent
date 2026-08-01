
def _trace(fn, inps) -> torch.fx.GraphModule:  # type: ignore[no-untyped-def]
    with dynamo_timed("fx.bucketing._trace", log_pt2_compile_event=True):
        fake_mode = detect_fake_mode(inps)
        assert fake_mode is not None
        with fake_mode, enable_python_dispatcher():
            out = make_fx(fn)(*inps)
            for node in out.graph.find_nodes(
                op="call_function", target=torch.ops.aten.detach.default
            ):
                node.replace_all_uses_with(node.args[0])
                out.graph.erase_node(node)
            return out


def _trace(*args, **kwargs):
    def wrapper(func):
        return torch.jit.trace(func, args, **kwargs)
    return wrapper


def _trace(func, args, operator_export_type, return_outs=False):
    # Special case for common case of passing a single Tensor
    if isinstance(args, torch.Tensor):
        args = (args,)

    trace_graph, torch_out, inputs_states = torch.jit._get_trace_graph(
        func,
        args,
        strict=False,
        _force_outplace=False,
        _return_inputs_states=True,
    )
    warn_on_static_input_change(inputs_states)

    trace_graph = _optimize_graph(trace_graph, operator_export_type, params_dict={})
    if return_outs:
        return trace_graph, torch_out
    return trace_graph


def _trace(A):
    # A compatibility function which should eventually disappear.
    if is_pydata_spmatrix(A):
        return A.to_scipy_sparse().trace()
    else:
        return A.trace()


def _trace(self: Array, offset: int | ArrayLike = 0, axis1: int = 0, axis2: int = 1,
           dtype: DTypeLike | None = None, out: None = None) -> Array:
  """Return the sum along the diagonal.

  Refer to :func:`jax.numpy.trace` for full documentation.
  """
  return lax_numpy.trace(self, offset=offset, axis1=axis1, axis2=axis2, dtype=dtype, out=out)

