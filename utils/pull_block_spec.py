import functools
from typing import Any, Callable

def pull_block_spec(
    f: Callable,
    out_block_specs: pallas_core.BlockSpec | tuple[pallas_core.BlockSpec, ...],
    *,
    scalar_prefetch_handler: Any | None = None,
    grid_len: int | None = None,
    strict_mode: bool = True,
):
  def wrapped(*args, **kwargs):
    jaxpr, consts, in_tree, out_tree_ = fuser_utils.make_jaxpr(
        f, *args, **kwargs
    )
    del out_tree_
    jaxpr_out_usages = [{Usage.REGULAR}] * len(jaxpr.outvars)
    block_specs_ = jax.tree.map(
        _unwrap_block_spec_scalar_prefetch, out_block_specs
    )
    flat_block_specs, out_tree = jax.tree.flatten(block_specs_)
    jaxpr, used_consts, used_invars = pe.dce_jaxpr_consts(
        jaxpr,
        used_outputs=[True] * len(jaxpr.outvars),
        instantiate=True,
    )
    assert all(used_invars)
    assert all(used_consts)
    read_usage_env = compute_usage(jaxpr, jaxpr_out_usages)
    in_block_specs, env = _pull_block_spec(
        jaxpr,
        tuple(flat_block_specs),
        scalar_prefetch_handler=scalar_prefetch_handler,
        read_usage_env=read_usage_env,
        grid_len=grid_len,
        strict_mode=strict_mode,
    )
    kernel_fn = make_kernel_function(
        jaxpr,
        consts,
        in_tree,
        out_tree,
        read_usage_env,
        in_block_specs,
        env,
        scalar_prefetch_handler,
        grid_len,
    )
    in_block_specs = jax.tree.unflatten(in_tree, in_block_specs)
    in_block_specs = jax.tree.map(
        functools.partial(
            _wrap_block_spec_scalar_prefetch,
            num_grid_args=grid_len,
        ),
        in_block_specs,
    )
    in_block_arg_specs, in_block_kwarg_specs = in_block_specs
    return kernel_fn, in_block_arg_specs, in_block_kwarg_specs

  return wrapped

