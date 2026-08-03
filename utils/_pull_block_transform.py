import functools
from typing import Any, Callable

def _pull_block_transform(
    jaxpr: core.Jaxpr,
    out_block_transforms: tuple[BlockIndexTransform, ...],
    *,
    read_usage_env: Callable[[core.Var], set[Usage]],
    scalar_prefetch_handler: Any | None = None,
    grid_len: int,
    strict_mode: bool = True,
) -> tuple[
    tuple[BlockIndexTransform, ...],
    tuple[dict[core.Var, BlockIndexTransform], dict[int, Any]],
]:
  jaxpr_invar_usages = util.safe_map(read_usage_env, jaxpr.invars)
  env: dict[core.Var, BlockIndexTransform] = {}
  scalar_prefetch_fn_env = {}

  block_idxs_avals = tuple(
      None
      if isinstance(out_block_transform, NoBlockIndexTransform)
      else (
          (jax._src.core.ShapedArray((), jnp.int32),)
          * len(out_block_transform.block_shape)
      )
      for out_block_transform in out_block_transforms
  )

  for outvar, bs in zip(jaxpr.outvars, out_block_transforms, strict=True):
    assert isinstance(outvar, core.Var)
    env[outvar] = bs

  def _read_block_spec(atom: core.Atom) -> BlockIndexTransform | Any:
    if isinstance(atom, core.Literal):
      return no_block_index_transform
    return env.get(atom, no_block_index_transform)

  def _write_block_spec(atom: core.Atom, block_transform: BlockIndexTransform):
    if isinstance(atom, core.Literal):
      return
    env[atom] = block_transform

  for i, eqn in reversed(list(enumerate(jaxpr.eqns))):
    eqn_out_block_transforms = tuple(util.safe_map(_read_block_spec, eqn.outvars))
    if all(bs is no_block_index_transform for bs in eqn_out_block_transforms):
      continue
    rule = pull_block_spec_rules.get(eqn.primitive, None)
    if not rule:
      raise NotImplementedError(eqn.primitive, eqn_out_block_transforms)
    ctx = PullRuleContext(
        avals_in=tuple(v.aval for v in eqn.invars),
        avals_out=tuple(v.aval for v in eqn.outvars),
        out_usages=tuple(read_usage_env(v) for v in jaxpr.outvars),
        scalar_prefetch_handler=scalar_prefetch_handler,
        grid_len=grid_len,
        strict_mode=strict_mode,
    )
    if eqn.primitive.multiple_results:
      in_block_transforms = rule(ctx, eqn_out_block_transforms, **eqn.params)
    else:
      in_block_transforms = rule(ctx, eqn_out_block_transforms[0], **eqn.params)

    eqn_invar_usages = [
        read_usage_env(v) if not isinstance(v, core.Literal) else set()
        for v in eqn.invars
    ]
    if any(Usage.SCALAR_PREFETCH in usage for usage in eqn_invar_usages):
      scalar_prefetch_vars = [
          Usage.SCALAR_PREFETCH in usage for usage in eqn_invar_usages
      ]
      needed_invars = [
          v
          for v, sp in zip(eqn.invars, scalar_prefetch_vars)
          if sp or isinstance(v, core.Literal)
      ]
      scalar_prefetch_jaxpr_no_dce = core.Jaxpr(
          jaxpr.constvars,
          jaxpr.invars,
          needed_invars,
          jaxpr.eqns[: jaxpr.eqns.index(eqn)],
          debug_info=jaxpr.debug_info._replace(result_paths=None),
      )
      scalar_prefetch_jaxpr, _, used_invars = pe.dce_jaxpr_consts(
          scalar_prefetch_jaxpr_no_dce,
          [True] * len(scalar_prefetch_jaxpr_no_dce.outvars),
      )
      assert not any(used_invars)
      scalar_prefetch_jaxpr = scalar_prefetch_jaxpr.replace(
          constvars=[],
          invars=jaxpr.constvars,
          debug_info=scalar_prefetch_jaxpr.debug_info.with_unknown_names(),
      )

      def _scalar_prefetch_fn(jaxpr):
        if grid_len is None:
          raise ValueError('Grid must be provided to pull_block_spec.')
        args = scalar_prefetch_handler(*_get_scalar_prefetch())
        # Load from SMEM
        args = [a[0] for a in args]
        return core.eval_jaxpr(jaxpr, [], *args)

      scalar_prefetch_fn = functools.partial(
          _scalar_prefetch_fn, scalar_prefetch_jaxpr
      )
      ctx.scalar_prefetch_fn = scalar_prefetch_fn_env[i] = scalar_prefetch_fn
    for v, in_block_transform in zip(eqn.invars, in_block_transforms, strict=True):
      if (
          not isinstance(v, core.Literal)
          and v in env
          and not _block_transforms_equal(
              env[v], in_block_transform, block_idxs_avals,
              strict_mode=strict_mode,
          )
      ):
        in_block_transform = BlockIndexTransform(_illegal, _illegal)
      _write_block_spec(v, in_block_transform)

  def _get_in_block_transforms(v, usage):
    if usage == {Usage.SCALAR_PREFETCH}:
      return None
    bs = env.get(v, no_block_index_transform)
    if bs is not no_block_index_transform:
      if bs.block_shape is _illegal:
        raise ValueError(
            'Fusion contains a DAG, cannot uniquely pull '
            f'block specs:\n{jaxpr}')
    return bs

  in_block_transforms = tuple(
      _get_in_block_transforms(v, usage)
      for v, usage in zip(jaxpr.invars, jaxpr_invar_usages)
  )

  return (
      in_block_transforms,
      (env, scalar_prefetch_fn_env),
  )

