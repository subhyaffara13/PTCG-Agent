import logging

def generate_and_save_checkpoint(
    config: configs.CheckpointConfig,
    output_dir: epath.PathLike,
    mesh: jax.sharding.Mesh | None = None,
) -> None:
  """Generates a synthetic checkpoint from a spec and writes it with `ocp.save`.

  Materialises a synthetic Orbax checkpoint on disk so a load benchmark has
  something to read without depending on a real model download. The fixture is
  deterministic for a fixed `config.random_seed`, which the digest-mode
  correctness check relies on.

  Args:
    config: The checkpoint config; must carry a `spec`.
    output_dir: Directory to write the Orbax checkpoint to.
    mesh: Mesh used to shard the generated data. If None, the data is not
      sharded.
  """
  out = epath.Path(output_dir)
  if out.exists() and any(out.iterdir()):
    logging.warning('A fixture is already present at %s; overwriting it.', out)
  pytree = generate_checkpoint(config, mesh=mesh)
  ocp.save(out, pytree, overwrite=True)

