
def _device_put_transpose(cts, *args, devices, srcs, copy_semantics):
  results: list[Any | None] = [None] * len(cts)
  dp_cts = []
  for i, (ct, arg, device, src, cp) in enumerate(zip(
      cts, args, devices, srcs, copy_semantics)):
    if ad.is_undefined_primal(arg):
      if type(ct) is ad.Zero:
        results[i] = ad.Zero(arg.aval)
      else:
        dp_cts.append((i, ct, arg, device, src, cp))

  if dp_cts:
    indices, dp_ct, args, devices, srcs, copy_semantics = list(zip(*dp_cts))
    # TODO(yashkatariya): Maybe remove the special carve out for Host?
    srcs = tuple(a.aval.memory_space
                 if s is None and a.aval.memory_space == core.MemorySpace.Host
                 else s for s, a in zip(srcs, args))
    new_copy_semantics = []
    for cp in copy_semantics:
      if cp == ArrayCopySemantics.DONATE_INPUT:
        raise ValueError(
            "donate=True is not allowed during tranposition of device_put."
            " Please file an issue if you want this to be supported.")
      elif cp == ArrayCopySemantics.REUSE_INPUT:
        new_copy_semantics.append(ArrayCopySemantics.ALWAYS_COPY)
      else:
        assert cp == ArrayCopySemantics.ALWAYS_COPY
        new_copy_semantics.append(ArrayCopySemantics.ALWAYS_COPY)
    ys = device_put_p.bind(*dp_ct, devices=srcs, srcs=devices,
                           copy_semantics=tuple(new_copy_semantics))
    for i, y in zip(indices, ys):
      results[i] = y
  return results

