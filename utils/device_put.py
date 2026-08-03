from typing import Any

def device_put(
    x,
    device: None | xc.Device | Sharding | P | Format | Any = None,
    *, src: None | xc.Device | Sharding | P | Format | Any = None,
    donate: bool | Any = False, may_alias: bool | None | Any = None):
  """Transfers ``x`` to ``device``.

  Args:
    x: An array, scalar, or (nested) standard Python container thereof.
    device: The (optional) :py:class:`Device`, :py:class:`Sharding`, or a
      (nested) :py:class:`Sharding` in standard Python container (must be a tree
      prefix of ``x``), representing the device(s) to which ``x`` should be
      transferred. If given, then the result is committed to the device(s).
    src: The (optional) :py:class:`Device`, :py:class:`Sharding`, or a (nested)
      :py:class:`Sharding` in standard Python container (must be a tree prefix
      of ``x``), representing the device(s) on which ``x`` belongs.
    donate: bool or a (nested) bool in standard Python container (must be a tree
      prefix of ``x``). If True, ``x`` can be overwritten and marked deleted in
      the caller. This is best effort. JAX will donate if possible, otherwise it
      won't. The input buffer (in the future) will always be deleted if donated.
    may_alias: bool or None or a (nested) bool in standard Python container
      (must be a tree prefix of ``x``). If False, `x` will be copied. If true,
      `x` may be aliased depending on the runtime's implementation.

  Returns:
    A copy of ``x`` that resides on ``device``.

  If the ``device`` parameter is ``None``, then this operation behaves like the
  identity function if the operand is on any device already, otherwise it
  transfers the data to the default device, uncommitted.

  This function is always asynchronous, i.e. returns immediately without
  blocking the calling Python thread until any transfers are completed.
  """
  with config.explicit_device_put_scope():
    x_flat, treedef = tree_flatten(x)
    x_avals = [shaped_abstractify(x) for x in x_flat]
    if (device is None or
        isinstance(device, (xc.Device, Sharding, core.MemorySpace))):
      device_flat = [device] * len(x_flat)
    else:
      device_flat = flatten_axes("device_put device", treedef, device)

    if (src is None or
        isinstance(src, (xc.Device, Sharding, core.MemorySpace))):
      src_flat = list(map(partial(_infer_src_sharding, src), x_flat, x_avals))
    else:
      src_flat = flatten_axes("device_put source", treedef, src)
      src_flat = list(map(_infer_src_sharding, src_flat, x_flat, x_avals))

    device_flat = map(partial(pspec_to_sharding, 'device_put'), device_flat)
    src_flat = map(partial(pspec_to_sharding, 'device_put'), src_flat)

    if isinstance(donate, bool):
      donate_flat = [donate] * len(x_flat)
    else:
      donate_flat = flatten_axes("device_put donate", treedef, donate)

    if isinstance(may_alias, bool):
      may_alias_flat = [may_alias] * len(x_flat)
    else:
      may_alias_flat = flatten_axes("device_put may_alias", treedef, may_alias)

    copy_semantics = []
    for m, d in zip(may_alias_flat, donate_flat):
      if m and d:
        raise ValueError('may_alias and donate cannot be True at the same time.')
      if m is None:
        m = not d
      if m and not d:
        copy_semantics.append(dispatch.ArrayCopySemantics.REUSE_INPUT)
      elif not m and d:
        copy_semantics.append(dispatch.ArrayCopySemantics.DONATE_INPUT)
      else:
        assert not m and not d
        copy_semantics.append(dispatch.ArrayCopySemantics.ALWAYS_COPY)

    dst_avals = []
    for x_aval, d in zip(x_avals, device_flat):
      aval = dispatch.update_dp_aval(x_aval, d)
      dst_avals.append(aval)
      _check_sharding(aval, d)
    if core.trace_state_clean():
      out_flat = dispatch._batched_device_put_impl(
          *x_flat, devices=device_flat, srcs=src_flat,
          copy_semantics=copy_semantics, dst_avals=dst_avals)
    else:
      out_flat = dispatch.device_put_p.bind(
          *x_flat, devices=tuple(device_flat), srcs=tuple(src_flat),
          copy_semantics=tuple(copy_semantics))
    return tree_unflatten(treedef, out_flat)

