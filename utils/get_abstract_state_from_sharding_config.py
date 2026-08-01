
def get_abstract_state_from_sharding_config(
    sharding_config_path: epath.Path,
    metadata: Any,
    *,
    devices: list[jax.Device],
) -> Any:
  """Loads abstract state from a JSON file."""
  path = epath.Path(sharding_config_path)
  parsed_config = json.loads(path.read_text())
  flat_abstract_state = {}
  for k, v in parsed_config.items():
    flat_abstract_state[k] = jax.ShapeDtypeStruct(
        shape=tuple(v['shape']),
        dtype=jnp.dtype(v['dtype']),
        sharding=jax.sharding.NamedSharding(
            mesh=jax.sharding.Mesh(
                np.array(devices).reshape(v['sharding']['mesh']['shape']),
                v['sharding']['mesh']['axes'],
            ),
            spec=jax.sharding.PartitionSpec(*v['sharding']['spec']),
        ),
    )
  return tree_utils.from_flat_dict(flat_abstract_state, metadata, sep='.')

