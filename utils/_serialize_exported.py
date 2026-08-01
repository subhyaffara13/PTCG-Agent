
def _serialize_exported(
    builder: flatbuffers.Builder, exp: _export.Exported, vjp_order: int
) -> int:
  uniques = _SerializedUniques.create_from_exported(exp)
  if not exp._has_named_shardings:
    raise ValueError(
      "Exported being serialized must have named shardings after 3/17/2026.")
  # Serialize bottom-up
  fun_name = builder.CreateString(exp.fun_name)
  in_tree = _serialize_pytreedef(builder, exp.in_tree)
  # TODO(necula): stop serializing in_avals 1 month after 4/4/26.
  in_avals = _serialize_array(builder, _serialize_aval, exp.in_avals)

  out_tree = _serialize_pytreedef(builder, exp.out_tree)
  # TODO(necula): stop serializing out_avals 1 month after 4/4/26
  out_avals = _serialize_array(builder, _serialize_aval, exp.out_avals)
  # TODO(necula): stop serializing in_shardings 1 month after 4/4/26
  in_shardings = _serialize_array(
      builder, partial(_serialize_sharding, uniques=uniques),
      exp._in_named_shardings)
  # TODO(necula): stop serializing out_shardings 1 month after 4/4/26
  out_shardings = _serialize_array(
      builder, partial(_serialize_sharding, uniques=uniques),
      exp._out_named_shardings)
  ordered_effects = _serialize_array(
      builder, _serialize_effect, exp.ordered_effects
  )
  unordered_effects = _serialize_array(
      builder, _serialize_effect, exp.unordered_effects
  )
  disabled_safety_checks = _serialize_array(
      builder, _serialize_disabled_safety_check, exp.disabled_safety_checks
  )
  platforms = _serialize_array(
      builder, lambda b, p: b.CreateString(p), exp.platforms
  )
  mlir_module_serialized = builder.CreateByteVector(exp.mlir_module_serialized)
  module_kept_var_idx = builder.CreateNumpyVector(
      np.array(exp.module_kept_var_idx, dtype=np.uint16)
  )

  vjp = None
  if vjp_order > 0:
    if not exp.has_vjp():
      # TODO: add test
      raise ValueError(
          "serialization of an Exported that does not have vjps of high-enough "
          "order"
      )
    vjp = _serialize_exported(builder, exp.vjp(), vjp_order - 1)

  unique_avals_offset = _serialize_array(
      builder, _serialize_aval, uniques.unique_avals)
  unique_abstract_meshes_offset = _serialize_array(
      builder, _serialize_abstract_mesh, uniques.unique_abstract_meshes)
  unique_named_shardings_offset = _serialize_array(
      builder, partial(_serialize_named_sharding, uniques=uniques),
      uniques.unique_named_shardings)

  in_aval_idxs = builder.CreateNumpyVector(
    np.array([uniques.avals_map[a] for a in exp.in_avals], dtype=np.uint32))
  out_aval_idxs = builder.CreateNumpyVector(
    np.array([uniques.avals_map[a] for a in exp.out_avals], dtype=np.uint32))

  in_shardings_idxs = builder.CreateNumpyVector(
    np.array([0 if s is None else 1 + uniques.named_shardings_map[s]
              for s in exp._in_named_shardings], dtype=np.uint32))
  out_shardings_idxs = builder.CreateNumpyVector(
    np.array([0 if s is None else 1 + uniques.named_shardings_map[s]
              for s in exp._out_named_shardings], dtype=np.uint32))

  ser_flatbuf.ExportedStart(builder)
  # TODO(necula): we cannot really store the actual serialization_version
  # in the flatbuffer because prior to 11/25/2025 deserializers checked
  # if the version is 2 or 3. I have now removed that check, but for the
  # sake of old deserializers we can only store version 3. Starting
  # on January 2026 we can store the actual version.
  ser_flatbuf.ExportedAddSerializationVersion(builder, 3)
  ser_flatbuf.ExportedAddFunctionName(builder, fun_name)
  ser_flatbuf.ExportedAddInTree(builder, in_tree)
  ser_flatbuf.ExportedAddInAvals(builder, in_avals)
  ser_flatbuf.ExportedAddOutTree(builder, out_tree)
  ser_flatbuf.ExportedAddOutAvals(builder, out_avals)
  ser_flatbuf.ExportedAddNrDevices(builder, exp.nr_devices)
  ser_flatbuf.ExportedAddInShardings(builder, in_shardings)
  ser_flatbuf.ExportedAddOutShardings(builder, out_shardings)
  ser_flatbuf.ExportedAddPlatforms(builder, platforms)
  ser_flatbuf.ExportedAddOrderedEffects(builder, ordered_effects)
  ser_flatbuf.ExportedAddUnorderedEffects(builder, unordered_effects)
  ser_flatbuf.ExportedAddDisabledChecks(builder, disabled_safety_checks)
  ser_flatbuf.ExportedAddMlirModuleSerialized(builder, mlir_module_serialized)
  ser_flatbuf.ExportedAddCallingConventionVersion(
      builder, exp.calling_convention_version
  )
  ser_flatbuf.ExportedAddModuleKeptVarIdx(builder, module_kept_var_idx)
  ser_flatbuf.ExportedAddUsesGlobalConstants(
      builder, exp.uses_global_constants
  )
  if vjp is not None:
    ser_flatbuf.ExportedAddVjp(builder, vjp)

  ser_flatbuf.ExportedAddUniqueAvals(builder, unique_avals_offset)
  ser_flatbuf.ExportedAddUniqueAbstractMeshes(builder,
                                              unique_abstract_meshes_offset)
  ser_flatbuf.ExportedAddUniqueNamedShardings(builder,
                                              unique_named_shardings_offset)
  ser_flatbuf.ExportedAddInAvalsIdxs(builder, in_aval_idxs)
  ser_flatbuf.ExportedAddOutAvalsIdxs(builder, out_aval_idxs)
  ser_flatbuf.ExportedAddInShardingsIdxs(builder, in_shardings_idxs)
  ser_flatbuf.ExportedAddOutShardingsIdxs(builder, out_shardings_idxs)

  return ser_flatbuf.ExportedEnd(builder)

