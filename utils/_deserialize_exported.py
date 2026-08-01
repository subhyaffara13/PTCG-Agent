
def _deserialize_exported(exp: ser_flatbuf.Exported) -> _export.Exported:
  scope = shape_poly.SymbolicScope(())  # TODO(necula): serialize the constraints

  unique_avals = [
      _deserialize_aval(exp.UniqueAvals(i), scope=scope, sharding=None)
      for i in range(exp.UniqueAvalsLength())]
  unique_abstract_meshes = [
      _deserialize_abstract_mesh(exp.UniqueAbstractMeshes(i))
      for i in range(exp.UniqueAbstractMeshesLength())
  ]
  uniques = _SerializedUniques.create_from_uniques(unique_avals,  # pyrefly: ignore[bad-argument-type]
                                                   unique_abstract_meshes,
                                                   [])
  unique_named_shardings = [
      _deserialize_named_sharding(exp.UniqueNamedShardings(i), uniques=uniques)
      for i in range(exp.UniqueNamedShardingsLength())
  ]
  uniques = _SerializedUniques.create_from_uniques(unique_avals,  # pyrefly: ignore[bad-argument-type]
                                                   unique_abstract_meshes,
                                                   unique_named_shardings)

  fun_name = exp.FunctionName().decode("utf-8")

  # TODO(necula): remove the fallback to NrDevicesShort and mark
  # the field "deprecated" once we abandon the old
  # serialization format (6 months after 11/24/2025).
  nr_devices = exp.NrDevices() or exp.NrDevicesShort()
  def sharding_by_idx(idx):
    if idx == 0:
      return None
    return uniques.unique_named_shardings[idx - 1]

  if exp.InShardingsIdxsLength() > 0:
    in_shardings = tuple(
        sharding_by_idx(exp.InShardingsIdxs(i))
        for i in range(exp.InShardingsIdxsLength())
    )
  elif exp.InShardingsLength() > 0:
    # TODO(necula): remove 6 months after 4/4/26
    in_shardings = tuple(
        _deserialize_sharding(exp.InShardings(i), uniques=uniques)
        for i in range(exp.InShardingsLength())
    )
  else:
    in_shardings = ()

  if exp.OutShardingsIdxsLength() > 0:
    out_shardings = tuple(
      sharding_by_idx(exp.OutShardingsIdxs(i))
      for i in range(exp.OutShardingsIdxsLength())
    )
  elif exp.OutShardingsLength() > 0:
    # TODO(necula): remove 6 months after 4/4/26
    out_shardings = tuple(
      _deserialize_sharding(exp.OutShardings(i), uniques=uniques)
      for i in range(exp.OutShardingsLength())
    )
  else:
    out_shardings = ()

  # has_named_sharding will be True for all exports created after 1/15/2026
  # TODO(b/489569164): remove has_named_sharding 6 months after 1/15/2026
  has_named_shardings = not any(isinstance(s, _export.HloSharding)
                                for s in itertools.chain(in_shardings, out_shardings))
  if has_named_shardings:
    def get_aval_by_idx(idx, sharding: _export.NamedSharding | None):
      base_aval = uniques.unique_avals[idx]
      if sharding is None:
        return base_aval
      return core.update_aval_with_sharding(base_aval, sharding)

    if exp.InAvalsIdxsLength() > 0:
      in_avals = tuple(
          get_aval_by_idx(exp.InAvalsIdxs(i), in_shardings[i])  # pyrefly: ignore[bad-argument-type]
          for i in range(exp.InAvalsIdxsLength()))
    elif exp.InAvalsLength() > 0:
      # TODO(necula): remove 6 months after 4/4/26
      in_avals = tuple(
          _deserialize_aval(exp.InAvals(i), scope=scope, sharding=in_shardings[i])  # pyrefly: ignore[bad-argument-type]
          for i in range(exp.InAvalsLength()))
    else:
      in_avals = ()

    if exp.OutAvalsIdxsLength() > 0:
      out_avals = tuple(
          get_aval_by_idx(exp.OutAvalsIdxs(i), out_shardings[i])  # pyrefly: ignore[bad-argument-type]
                          for i in range(exp.OutAvalsIdxsLength()))
    elif exp.OutAvalsLength() > 0:
      # TODO(necula): remove 6 months after 4/4/26
      out_avals = tuple(
        _deserialize_aval(exp.OutAvals(i), scope=scope, sharding=out_shardings[i])  # pyrefly: ignore[bad-argument-type]
        for i in range(exp.OutAvalsLength())
      )
    else:
      out_avals = ()

    in_shardings_hlo = tuple(_export.named_to_hlo_sharding(s, aval)  # pyrefly: ignore[bad-argument-type]
                             for s, aval in zip(in_shardings, in_avals))
    out_shardings_hlo = tuple(_export.named_to_hlo_sharding(s, aval)  # pyrefly: ignore[bad-argument-type]
                             for s, aval in zip(out_shardings, out_avals))
  else:
    # Export from before 1/15/26
    in_avals = tuple(
        _deserialize_aval(exp.InAvals(i), scope=scope, sharding=None)
        for i in range(exp.InAvalsLength())
    )
    out_avals = tuple(
        _deserialize_aval(exp.OutAvals(i), scope=scope, sharding=None)
        for i in range(exp.OutAvalsLength())
    )
    in_shardings_hlo = cast(tuple[_export.HloSharding | None, ...], in_shardings)
    in_shardings = (None,) * len(in_shardings)
    out_shardings_hlo = cast(tuple[_export.HloSharding | None, ...], out_shardings)
    out_shardings = (None,) * len(out_shardings)

  in_tree = _deserialize_pytreedef(exp.InTree(), in_avals)
  out_tree = _deserialize_pytreedef(exp.OutTree(), out_avals)

  platforms = tuple(
      exp.Platforms(i).decode("utf-8")
      for i in range(exp.PlatformsLength())
  )
  ordered_effects = tuple(
      _deserialize_effect(exp.OrderedEffects(i))
      for i in range(exp.OrderedEffectsLength())
  )
  unordered_effects = tuple(
      _deserialize_effect(exp.UnorderedEffects(i))
      for i in range(exp.UnorderedEffectsLength())
  )
  disabled_safety_checks = tuple(
      _deserialize_disabled_safety_check(exp.DisabledChecks(i))
      for i in range(exp.DisabledChecksLength())
  )

  mlir_module_serialized = exp.MlirModuleSerializedAsNumpy().tobytes()
  calling_convention_version = exp.CallingConventionVersion()
  module_kept_var_idx = tuple(exp.ModuleKeptVarIdxAsNumpy().tolist())
  uses_global_constants = exp.UsesGlobalConstants()

  _get_vjp = None
  if vjp := exp.Vjp():
    _get_vjp = lambda _: _deserialize_exported(vjp)

  return _export.Exported(
      fun_name=fun_name,
      in_tree=in_tree,
      in_avals=in_avals,
      out_tree=out_tree,
      out_avals=out_avals,
      nr_devices=nr_devices,
      in_shardings_hlo=in_shardings_hlo,
      out_shardings_hlo=out_shardings_hlo,
      _has_named_shardings=has_named_shardings,
      _in_named_shardings=in_shardings,  # pyrefly: ignore[bad-argument-type]
      _out_named_shardings=out_shardings,  # pyrefly: ignore[bad-argument-type]
      platforms=platforms,
      ordered_effects=ordered_effects,
      unordered_effects=unordered_effects,
      disabled_safety_checks=disabled_safety_checks,
      mlir_module_serialized=mlir_module_serialized,
      calling_convention_version=calling_convention_version,
      module_kept_var_idx=module_kept_var_idx,
      uses_global_constants=uses_global_constants,
      _get_vjp=_get_vjp,
  )

