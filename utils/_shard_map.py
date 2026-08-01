
def _shard_map(f: F, *, mesh: Mesh | AbstractMesh | None,
               in_specs: Specs, out_specs: Specs, axis_names: Set[AxisName],
               check_vma: bool, _smap: bool = False) -> F:
  if not callable(f):
    raise TypeError("shard_map requires a callable for its first argument, "
                    f"but got {f} of type {type(f)}.")

  @util.wraps(f)
  @traceback_util.api_boundary
  def wrapped(*args):
    nonlocal mesh, axis_names
    mesh, axis_names = _shmap_checks(
        mesh, axis_names, in_specs, out_specs, _smap)
    dbg = api_util.debug_info("shard_map", f, args, {})
    args_flat = FlatTree.flatten(args)
    api_util.check_no_transformed_refs_args(lambda: dbg, args_flat)

    try:
      in_specs_flat = broadcast_prefix(
          in_specs, args, is_leaf=lambda x: x is None)
    except ValueError:
      e, *_ = prefix_errors(in_specs, args)
      raise e('shard_map in_specs') from None

    if (in_specs is Infer and
        all(mesh._name_to_type[a] == AxisType.Explicit for a in axis_names)):
      arg_s = [typeof(a).sharding for a in args_flat]
      assert all(i is Infer for i in in_specs_flat), in_specs_flat
      in_specs_flat = [_manual_spec(axis_names, s.spec, mesh) for s in arg_s]

    in_tree = args_flat.tree
    which_dyn = [s is not None for s in in_specs_flat]
    static_args   = [x for x, dyn in zip(args_flat, which_dyn) if not dyn]
    dyn_args      = [x for x, dyn in zip(args_flat, which_dyn) if dyn]
    in_specs_flat = tuple(s for s, dyn in zip(in_specs_flat, which_dyn) if dyn)
    dyn_argnums   = [i for i, dyn in enumerate(which_dyn) if dyn]
    _check_specs_vs_args(f, mesh, in_tree, in_specs, dyn_argnums,
                         in_specs_flat, dyn_args)

    # TODO(yashkatariya): Add support for partial manual
    mesh_axis_names_wo_vmap = (
        frozenset(mesh.axis_names) - core.get_axis_env().explicit_mesh_axis_names)
    if (mesh_axis_names_wo_vmap == axis_names and
        all(mesh._name_to_type[a] == AxisType.Explicit for a in axis_names)):
      for a, s in zip(dyn_args, in_specs_flat):
        if not isinstance(s, P): continue
        arg_aval = typeof(a)
        s = s._normalized_spec_for_aval(arg_aval.ndim)
        if config.remove_size_one_mesh_axis_from_type.value:
          s = remove_size_one_mesh_axis(s, mesh)
        if arg_aval.sharding.spec != s:
          raise ValueError(
              f"in_specs passed to shard_map: {s} does not match the specs of"
              f" the input: {arg_aval.sharding.spec} for arg: {typeof(a)}."
              " `in_specs` is an optional argument so you can omit specifying"
              " it and shard_map will infer the in_specs from the arguments."
              " If you want to reshard your inputs, you can use `jax.reshard`"
              " on the arguments and then pass those args to shard_map.")

    if (dbg.arg_names is not None and len(dyn_args) != len(dbg.arg_names)):
      dbg = dbg.with_unknown_names()

    def f_wrapped(*dyn_args):
      dyn_args_iter = iter(dyn_args)
      static_args_iter = iter(static_args)
      all_args = [next(dyn_args_iter) if dyn else next(static_args_iter)
                  for dyn in which_dyn]
      args = tree_unflatten(in_tree, all_args)
      ans = f(*args)
      ans_ft = FlatTree.flatten(ans)
      try:
        out_specs_flat = tuple(broadcast_prefix(out_specs, ans))
      except ValueError:
        e, *_ = prefix_errors(out_specs, ans)
        raise e('shard_map out_specs') from None
      def add_implicit_pvary_and_unreduced(val, spec):
        if not config.auto_pcast.value:
          return val
        if not isinstance(spec, P):
          return val
        aval = typeof(val)
        val = pvary(val, tuple(_spec_to_vma(spec) - aval.mat.varying))
        return (lax_parallel.vary_unreduced_cast(val, tuple(unreduced))
                if (unreduced := spec.unreduced - aval.mat.unreduced) else val)
      if check_vma:
        ans_ft = ans_ft.map2(add_implicit_pvary_and_unreduced, out_specs_flat)
      return ans_ft.with_aux(out_specs_flat)

    try:
      newly_manual_axes = axis_names - set(mesh.manual_axes)
      out_ft = shard_map_p.bind(
          *dyn_args, subfuns=(f_wrapped,), mesh=mesh, in_specs=in_specs_flat,
          check_vma=check_vma, newly_manual_axes=newly_manual_axes, debug_info=dbg)
    except _SpecError as e:
      fails, out_tree = e.args
      msg = _spec_rank_error(SpecErrorType.out, f, out_tree, out_specs, fails)
      if any(fail is not no_fail and not fail.shape for fail in fails):
        msg += (" In particular, for rank 0 outputs which are not constant "
                "over the mesh, add at least one (singleton) axis to them so "
                "that they can be concatenated using out_specs.")
      raise ValueError(msg) from None
    except _RepError as e:
      fails, out_tree, = e.args
      msg = _inout_vma_error(f, mesh, out_tree, out_specs, fails)
      raise ValueError(msg) from None
    return out_ft.unflatten()
  return cast(F, wrapped)

